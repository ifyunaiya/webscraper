from decimal import Decimal
from unittest.mock import AsyncMock, patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from pages.models import PriceWatch
from pages.scraper import parse


class ProductParsingTests(TestCase):
	def test_parse_returns_product_card_fields_and_image(self):
		data = {
			"product": {
				"detail": {
					"colors": [{
						"name": "Black",
						"xmedia": [{
							"extraInfo": {"deliveryUrl": "https://static.zara.test/item.jpg"}
						}],
					}],
				},
			},
			"productMetaData": [{
				"sku": "item-black-m",
				"name": "LINEN SHIRT",
				"price": 29.99,
				"availability": "in_stock",
				"url": "https://www.zara.com/uk/en/item.html",
				"sizeName": "M",
				"colorName": "Black",
				"description": "A linen shirt",
			}],
		}

		self.assertEqual(parse(data), [{
			"sku": "item-black-m",
			"name": "LINEN SHIRT",
			"price": 29.99,
			"url": "https://www.zara.com/uk/en/item.html",
			"sizeName": "M",
			"colorName": "Black",
			"description": "A linen shirt",
			"image_url": "https://static.zara.test/item.jpg",
		}])


class PriceWatchViewTests(TestCase):
	@patch("pages.views.main", new_callable=AsyncMock)
	def test_search_renders_product_cards(self, scraper):
		scraper.return_value = [{
			"sku": "item-black-m",
			"name": "LINEN SHIRT",
			"price": 29.99,
			"url": "https://www.zara.com/uk/en/item.html",
			"sizeName": "M",
			"colorName": "Black",
			"description": "A linen shirt",
			"image_url": "https://static.zara.test/item.jpg",
		}]

		response = self.client.post(reverse("run_function"), {
			"qsearch": "https://www.zara.com/uk/en/item.html",
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "LINEN SHIRT")
		self.assertContains(response, "Set price alert")
		scraper.assert_awaited_once_with("https://www.zara.com/uk/en/item.html")

	@patch("pages.views.main", new_callable=AsyncMock)
	def test_alert_saves_selected_variant(self, scraper):
		scraper.return_value = [{
			"sku": "item-black-m",
			"name": "LINEN SHIRT",
			"price": 29.99,
			"sizeName": "M",
			"colorName": "Black",
		}]

		response = self.client.post(reverse("create_watch"), {
			"product_url": "https://www.zara.com/uk/en/item.html",
			"sku": "item-black-m",
			"color_name": "Black",
			"size_name": "M",
			"target_price": "25.00",
			"email": "buyer@example.com",
		})

		watch = PriceWatch.objects.get()
		self.assertRedirects(response, reverse("home"))
		self.assertEqual(watch.product_name, "LINEN SHIRT")
		self.assertEqual(watch.current_price, Decimal("29.99"))
		self.assertEqual(watch.target_price, Decimal("25.00"))


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PriceWatchCommandTests(TestCase):
	@patch("pages.management.commands.check_price_watches.main", new_callable=AsyncMock)
	def test_notifies_once_when_price_reaches_target(self, scraper):
		scraper.return_value = [{"sku": "item-black-m", "price": 24.50}]
		watch = PriceWatch.objects.create(
			product_url="https://www.zara.com/uk/en/item.html",
			product_name="LINEN SHIRT",
			sku="item-black-m",
			color_name="Black",
			size_name="M",
			email="buyer@example.com",
			target_price=25,
			current_price=29.99,
		)

		from django.core.management import call_command
		call_command("check_price_watches")

		watch.refresh_from_db()
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].to, ["buyer@example.com"])
		self.assertFalse(watch.active)
		self.assertIsNotNone(watch.notified_at)
		self.assertEqual(watch.current_price, Decimal("24.50"))

	@patch("pages.management.commands.check_price_watches.main", new_callable=AsyncMock)
	def test_does_not_notify_above_target(self, scraper):
		scraper.return_value = [{"sku": "item-black-m", "price": 29.99}]
		watch = PriceWatch.objects.create(
			product_url="https://www.zara.com/uk/en/item.html",
			product_name="LINEN SHIRT",
			sku="item-black-m",
			email="buyer@example.com",
			target_price=25,
			current_price=29.99,
		)

		from django.core.management import call_command
		call_command("check_price_watches")

		watch.refresh_from_db()
		self.assertEqual(len(mail.outbox), 0)
		self.assertTrue(watch.active)
		self.assertEqual(watch.current_price, Decimal("29.99"))

	@patch("pages.management.commands.check_price_watches.send_mail", side_effect=OSError("SMTP unavailable"))
	@patch("pages.management.commands.check_price_watches.main", new_callable=AsyncMock)
	def test_keeps_alert_active_when_email_fails(self, scraper, send_email):
		scraper.return_value = [{"sku": "item-black-m", "price": 24.50}]
		watch = PriceWatch.objects.create(
			product_url="https://www.zara.com/uk/en/item.html",
			product_name="LINEN SHIRT",
			sku="item-black-m",
			email="buyer@example.com",
			target_price=25,
			current_price=29.99,
		)

		from django.core.management import call_command
		call_command("check_price_watches", stderr=None)

		watch.refresh_from_db()
		self.assertTrue(watch.active)
		self.assertIsNone(watch.notified_at)
		send_email.assert_called_once()

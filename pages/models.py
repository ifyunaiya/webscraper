from django.db import models


class PriceWatch(models.Model):
	product_url = models.URLField(max_length=500)
	product_name = models.CharField(max_length=200)
	sku = models.CharField(max_length=100, blank=True)
	color_name = models.CharField(max_length=100, blank=True)
	size_name = models.CharField(max_length=100, blank=True)
	email = models.EmailField()
	target_price = models.DecimalField(max_digits=10, decimal_places=2)
	current_price = models.DecimalField(max_digits=10, decimal_places=2)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	notified_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.product_name} below {self.target_price}"

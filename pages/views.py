# import asyncio
# from decimal import Decimal, InvalidOperation
# from urllib.parse import urlsplit

# import aiohttp
# from django.conf import settings
# from django.contrib import messages
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from django.shortcuts import get_object_or_404, redirect, render
# from django.views.decorators.http import require_POST

# from .models import PriceWatch
# from .scraper import main

from django.shortcuts import render
from django.views.decorators.http import require_POST
from asgiref.sync import async_to_sync
from urllib.parse import urlparse

from . import scraper




def home(request):
    return render(request, "home.html")

@require_POST
def find_product(request):

    product_url = request.POST.get('product_url').strip()

    # Check that a URL was submitted
    if not product_url:
        return render(request, 'product_preview.html', {
            'error': 'Please enter a product URL.'
        })

    # Check that the URL belongs to Zara

    # Call your asynchronous scraper

    # Handle unexpected scraper errors



    # Process the Zara product URL here

    return render(request, 'product_preview.html', {
        'product_url': product_url
    })

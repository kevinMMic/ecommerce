# products/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()  # Fetch all products

    # Handle sorting based on query parameters
    sort_order = request.GET.get('sort')  # Get the sort parameter from the request
    if sort_order == 'price_asc':
        products = products.order_by('price')  # Sort by price ascending
    elif sort_order == 'price_desc':
        products = products.order_by('-price')  # Sort by price descending

    return render(request, 'product_list.html', {'products': products})

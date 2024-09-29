import requests
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Fetch products from Fake Store API'

    def handle(self, *args, **kwargs):
        response = requests.get('https://fakestoreapi.com/products')
        products = response.json()

        for product in products:
            Product.objects.create(
                title=product['title'],
                price=product['price'],
                description=product['description'],
                image=product['image'],
                category=product['category']
            )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved products!'))

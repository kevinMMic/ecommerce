# views.py

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
from  cart.models import CartItem
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(request):
    if request.method == 'POST':
        YOUR_DOMAIN = "http://localhost:8000"  # Change to your domain
        
        # Initialize an empty list for line items
        line_items = []

        # Get cart items based on authentication status
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            # For non-authenticated users, get cart items from the session
            cart = request.session.get('cart', {})
            for item in cart.values():
                if 'product_id' in item:
                    product = get_object_or_404(Product, id=item['product_id'])  # Fetch product details
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product.title,  # Ensure the Product model has a title
                                'images': [product.image],  # Ensure the Product model has an image URL
                            },
                            'unit_amount': int(product.price * 100),  # Assuming the price is in dollars
                        },
                        'quantity': item['quantity'],  # Use the quantity from the session
                    })

        # Check if line items exist
        if not line_items:
            return JsonResponse({'error': 'No items in cart.'}, status=400)

        # Create Stripe checkout session with the actual line items
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({'id': checkout_session.id})
    
def payment_success(request):
    # Render success page
    return render(request, 'payment/success.html')

def payment_cancel(request):
    # Render cancel page
    return render(request, 'payment/cancel.html')

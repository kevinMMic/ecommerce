# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import CartItem
from products.models import Product  # Import Product model
from django.conf import settings

def add_to_cart(request, product_id):
    # Get the product object
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Check if the item already exists in the cart for authenticated users
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}  # Set default quantity if creating a new entry
        )
        if not created:  # If the cart item already exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
    else:
        # Handle anonymous users using session-based cart
        cart = request.session.get('cart', {})  # Initialize cart if it doesn't exist

        # Check if the product is already in the session cart
        if str(product.id) in cart:
            cart[str(product.id)]['quantity'] += 1  # Increment quantity
        else:
            # Add new item with product_id and quantity
            cart[str(product.id)] = {'product_id': product.id, 'quantity': 1}
            
        request.session['cart'] = cart  # Save back to session

    # Redirect to cart or product page
    return redirect('view_cart')

def view_cart(request):
    cart_items = []
    total_price = 0
    
    if request.user.is_authenticated:
        # For authenticated users, get cart items from the database
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # For anonymous users, get cart items from the session
        cart = request.session.get('cart', {})
        
        for item in cart.values():
            if 'product_id' in item:
                product = get_object_or_404(Product, id=item['product_id'])  # Fetch product details
                cart_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'product_id': item['product_id'],  # Add product_id to be used in forms
                })
    
    # Calculate total price
    total_price = sum(item['product'].price * item['quantity'] for item in cart_items)
    
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def update_quantity(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            # For authenticated users, update CartItem in the database
            cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
        else:
            # For anonymous users, update session-based cart
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] = quantity
                request.session['cart'] = cart  # Save back to session

    return redirect('view_cart')

def delete_cart_item(request, product_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # For authenticated users, delete from the database
            cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
            cart_item.delete()
        else:
            # For anonymous users, delete from session-based cart
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session['cart'] = cart  # Save back to session

    return redirect('view_cart')

def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # Handle session-based cart for non-authenticated users
        cart = request.session.get('cart', {})
        cart_items = []  # Create an empty list to store cart items
        for item in cart.values():
            try:
                product = get_object_or_404(Product, id=item['product_id'])  # Ensure item has product_id
                cart_items.append({'product': product, 'quantity': item['quantity']})
            except KeyError:
                # Log an error or handle the case where product_id is missing
                print("KeyError: 'product_id' is missing in cart item:", item)

    # Check if cart is empty
    if not cart_items:
        return render(request, 'cart/checkout.html', {
            'error': 'No items in cart.',
            'STRIPE_TEST_PUBLIC_KEY': settings.STRIPE_TEST_PUBLIC_KEY
        })

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,  # Pass the cart items to the template
        'STRIPE_TEST_PUBLIC_KEY': settings.STRIPE_TEST_PUBLIC_KEY
    })

from django.urls import path
from django.contrib import admin
from products.views import product_list
from cart.views import view_cart, add_to_cart, update_quantity, delete_cart_item, checkout
from payments.views import create_checkout_session, payment_success, payment_cancel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list, name='product_list'),
    path('cart/', view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:product_id>/', update_quantity, name='update_quantity'),
    path('delete/<int:product_id>/', delete_cart_item, name='delete_cart_item'),  # Use product_id
    path('checkout/', checkout, name='checkout'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('success/', payment_success, name='payment_success'),
    path('cancel/', payment_cancel, name='payment_cancel'),
]

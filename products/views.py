from __future__ import unicode_literals

from django.shortcuts import render
from .models import Product
from shopping_cart.models import Order
from django.urls import reverse_lazy


# from django.views.generic import CreateView 
# from django.shortcuts import get_object_or_404
# from django.urls import reverse_lazy

# class ProductCreateView(CreateView):
#     model = Product
#     fields= '__all__'
#     success_url = reverse_lazy('product_list')

def product_list(request):
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "products/product_list.html", context)
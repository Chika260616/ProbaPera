from django.urls import path
from shopping_cart import views

app_name = 'shopping_cart'

urlpatterns = [
    path('add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    path('order-summary/$', views.order_details, name="order_summary"),
    path('success/$', views.success, name='purchase_success'),
    path('item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
    path('checkout/$', views.checkout, name='checkout'),
    path('payment/(?P<order_id>[-\w]+)/$', views.process_payment, name='process_payment'),
    path('update-transaction/(?P<order_id>[-\w]+)/$', views.update_transaction_records, name='update_records'),

]
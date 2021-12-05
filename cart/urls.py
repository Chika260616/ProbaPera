from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('admin/', admin.site.urls),
    url('profiles/', include('accounts.urls')),
    url('products/', include('products.urls')),
    url('cart/', include('shopping_cart.urls'))
]

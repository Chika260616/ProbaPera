from django.shortcuts import render, get_object_or_404

from shopping_cart.models import Order
from .models import Profile

from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

def my_profile(request):
	my_user_profile = Profile.objects.filter(user=request.user).first()
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
	context = {
		'my_orders': my_orders
	}

	return render(request, "profile.html", context)



class SignUpView(CreateView):

    template_name = 'accounts/signup.html'

    form_class = UserCreationForm

    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)

        return to_return

class CustomLoginView(LoginView):

    template_name = 'accounts/login.html'


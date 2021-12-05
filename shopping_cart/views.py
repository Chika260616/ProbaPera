import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Profile
from products.models import Product

from shopping_cart.extras import generate_order_id
from shopping_cart.models import OrderItem, Order


def get_user_pending_order(request):
    # получить заказ для нужного пользователя
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # получить единственный заказ в списке отфильтрованных заказов
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # получить профиль пользователя
    user_profile = get_object_or_404(Profile, user=request.user)
    # фильтровать продукты по идентификатору
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # проверить, владеет ли пользователь уже этим продуктом
    if product in request.user.profile.ebooks.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('products:product-list')) 
    # создать OrderItem выбранного продукта
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # создать заказ, связанный с пользователем
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # генерировать справочный код
        user_order.ref_code = generate_order_id()
        user_order.save()

    # показать подтверждающее сообщение и перенаправить обратно на ту же страницу
    messages.info(request, "item added to cart")
    return redirect(reverse('shopping_cart:order_summary'))

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required()
def checkout(request):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order,
    }
    return render(request, 'shopping_cart/checkout.html', context)


@login_required()
def process_payment(request, order_id):
    # обработать платеж
    return redirect(reverse('shopping_cart:update_records',
                    kwargs={
                        'order_id': order_id,
                    })
                )


@login_required()
def update_transaction_records(request, order_id):
    # получить обрабатываемый заказ
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    # обновить размещенный заказ
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # получить все элементы в порядке - формирует набор запросов
    order_items = order_to_purchase.items.all()

    # обновление элементов заказа
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Добавление продуктов в профиль пользователя
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()

    #====== TODO: Update Payment records ========

    # отправить электронное письмо клиенту
    messages.info(request, "Thank you! Your items have been added to your profile")
    return redirect(reverse('accounts:my_profile'))


def success(request, **kwargs):
    # представление, означающее, что транскрипция прошла успешно
    return render(request, 'shopping_cart/purchase_success.html', {})

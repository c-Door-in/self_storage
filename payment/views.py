from datetime import datetime, timedelta

import stripe
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from store.models import Box, Customer
from django.contrib.auth.models import User
from django.urls import reverse_lazy


def make_payment(request, box_pk):
    user_id = request.user.id
    box = Box.objects.get(pk=box_pk)
    stripe.api_key = settings.STRIPE_API_KEY

    amount =  int(box.price)*100

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Вы арендуете бокс по адресу {box.storage.location_street_name}, {box.storage.location_street_number}',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        metadata = {
            'user_id': user_id,
            'box_pk': box_pk,
        },
        success_url=request.build_absolute_uri(reverse('payment:successed_payment')),
        cancel_url=request.build_absolute_uri(reverse('payment:cancelled_payment')),
    )

    return redirect(session.url, code=303)


def pay_success(request):
    stripe.api_key = settings.STRIPE_API_KEY
    stripe_sessions = stripe.checkout.Session.list(limit=3)
    session = stripe_sessions['data'][0]
    if session['payment_status'] == 'paid':
        user_id = session['metadata']['user_id']
        box_pk = session['metadata']['box_pk']
        customer, created = Customer.objects.get_or_create(user__id=user_id)
        box = Box.objects.get(pk=box_pk)
        box.customer = customer
        box.in_use = True
        box.rental_start_time = datetime.now()
        box.rental_end_time = datetime.now() + timedelta(days=30)
        box.save()
    user_id = request.user.id

    return render(request, 'success.html')


# def cancelled(request):
#     user_id = request.user.id
#     # sub_type = order['sub_type']
#     print(user_id)
#     print(request)
#     print(request.session)

#     return redirect('store:my_rent')


@login_required
def cancelled(request):
    return render(request, 'cancelled.html')


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


# class OrderView(TemplateView):
#     template_name = 'order.html'

#     def dispatch(self, request, *args, **kwargs):
#         user_id = request.user.id
#         request.session[str(user_id)] = {
#             'subscriber_id': 1,
#             'preference_id': 2,
#             'allergy_id': 2,
#             'number_of_meals': 3,
#             'persons_quantity': 1,
#             'shown_dishes_id': 1,
#             'sub_type': 12,             
#             }
#         return super(OrderView, self).dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_id = self.request.user.id
#         # TODO можно формирование словаря для подписки засунуть сюда
#         return context

from datetime import datetime

import stripe
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.conf import settings
from website.models import Subscribe, Allergy
from django.contrib.auth.models import User


def make_payment(request):
    stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY

    amount =  5000

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Ваш заказ №',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('successed_payment')),
        cancel_url=request.build_absolute_uri(reverse('cancelled_payment')),
    )

    return redirect(session.url, code=303)


def pay_success(request):
    user_id = request.user.id
    order = request.session[f'sub_{str(user_id)}']
    sub_type = order['sub_type']
    subscribe = Subscribe.objects.create(
        title=f'Подписка на {sub_type} месяцев от {datetime.now().date()}',
        subscriber=User.objects.get(pk=user_id),
        number_of_meals=order['number_of_meals'],
        persons_quantity=order['persons_quantity'],
        sub_type=sub_type,
    )
    if order['allergies']:
        for allergy in order['allergies']:
            subscribe.allergy.add(Allergy.objects.get(title=allergy))

    del request.session[f'sub_{str(user_id)}']

    return render(request, "success.html")


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


class OrderView(TemplateView):
    template_name = 'order.html'

    def dispatch(self, request, *args, **kwargs):
        user_id = request.user.id
        request.session[str(user_id)] = {
            'subscriber_id': 1,
            'preference_id': 2,
            'allergy_id': 2,
            'number_of_meals': 3,
            'persons_quantity': 1,
            'shown_dishes_id': 1,
            'sub_type': 12,             
            }
        return super(OrderView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        # TODO можно формирование словаря для подписки засунуть сюда
        return context

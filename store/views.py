from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from store.models import Storage, Customer, Application, Box, User

import datetime
import pytz

def save_email_if_sent(request):
    email = request.GET.get('EMAIL1')
    if not email:
        return
    # save email if valid else pass


def index(request):
    save_email_if_sent(request)
    return render(request, 'index.html')


def boxes(request):
    save_email_if_sent(request)
    return render(request, 'boxes.html')


@login_required
def my_rent(request):

    username = request.user
    user = User.objects.get(username=username)
    customer = user.customer
    user_boxes = customer.rented_boxes.all()
    user_boxes_data = []
    timezone = 'Europe/Moscow'

    for box in user_boxes:
        time_now = datetime.datetime.now(pytz.timezone(timezone))
        rental_end_time = (box.rental_end_time).astimezone(pytz.timezone(timezone))
        time_left = rental_end_time - time_now
        warning = None
        if time_left.days <= 5:
            warning = f'Срок Вашей аренды подходит к концу :( \n Вы можете продлить аренду или забрать вещи до {rental_end_time} включительно.'

        storage = box.storage
        user_boxes_data.append(
            {
                'storage_number': storage.id,
                'storage_location_city': storage.location_city,
                'storage_location_street_name': storage.location_street_name,
                'storage_location_street_number': storage.location_street_number,
                'number': box.number,
                'rental_start_time': box.rental_start_time,
                'rental_end_time': box.rental_end_time,
                'warning': warning
            }
        )

    user_data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'image_url': customer.photo.url,
        'password': user.password,
        'email': user.email,
        'phone_number': customer.phone_number,
    }

    if user_boxes:
        user_data.update(user_boxes=user_boxes_data)
        return render(request, 'my-rent.html', context=user_data)

    else:
        note = 'У вас еще нет аренды :( ' \
               'Но вы можете арендовать свой первый бокс  по  привлекательной цене прямо сейчас'
        user_data.update(note=note)
        return render(request, 'my-rent-empty.html', context=user_data)




def faq(request):
    return render(request, 'faq.html')


@login_required
def payment(request):
    return render(request, 'index.html')


@login_required
def log_out(request):
    logout(request)
    return redirect(index)

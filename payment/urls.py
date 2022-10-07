from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('success/', views.pay_success, name='successed_payment'),
    path('cancelled/', views.cancelled, name='cancelled_payment'),
    path('', views.make_payment, name='make_payment'),
]
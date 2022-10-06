from django.urls import path
from . import views


urlpatterns = [
    path('success/', views.pay_success, name='successed_payment'),
    path('cancelled/', views.CancelledView.as_view(), name='cancelled_payment'),
    path('make/', views.make_payment, name='make_payment'),
]
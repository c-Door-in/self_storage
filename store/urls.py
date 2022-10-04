from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('boxes/', views.boxes, name='boxes'),
    path('my_rent/', views.my_rent, name='my_rent'),
    path('faq/', views.faq, name='faq'),
]

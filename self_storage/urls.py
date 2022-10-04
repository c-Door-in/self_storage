from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('boxes/', views.boxes),
    path('my_rent/', views.my_rent),
    path('my_rent_empty/', views.my_rent_empty),
    path('faq/', views.faq),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

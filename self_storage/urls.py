from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('boxes/', views.boxes, name='boxes'),
    path('my_rent/', views.my_rent, name='my_rent'),
    path('faq/', views.faq, name='faq'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

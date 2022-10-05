from django.contrib import admin
from .models import Application, Customer, Storage, Box

admin.site.register(Application)
admin.site.register(Customer)
admin.site.register(Storage)
admin.site.register(Box)



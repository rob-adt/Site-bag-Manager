from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

admin.site.register(Bag)
admin.site.register(Employee)
admin.site.register(Borrowingtime)
admin.site.register(Tags)
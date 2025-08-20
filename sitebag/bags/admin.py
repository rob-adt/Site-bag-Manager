from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

admin.site.register(Bags)
admin.site.register(Employees)
admin.site.register(Borrowingtime)
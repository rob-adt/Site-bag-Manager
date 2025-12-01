from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']

class BagAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tagg']

admin.site.register(Bag, BagAdmin)
admin.site.register(Employee)
admin.site.register(Borrowingtime)
admin.site.register(Tags, TagAdmin)
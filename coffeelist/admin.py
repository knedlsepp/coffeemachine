from django.contrib import admin

# Register your models here.
from coffeelist.models import *

admin.site.register(Tag)
admin.site.register(Purchase)
admin.site.register(Deposit)
admin.site.register(Price)

from django.contrib import admin
from .models import Groups, Elements, StoreTown, ElementIntown
# Register your models here.

admin.site.register(Groups)
admin.site.register(Elements)
admin.site.register(StoreTown)
admin.site.register(ElementIntown)

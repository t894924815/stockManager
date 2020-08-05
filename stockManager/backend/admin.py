from django.contrib import admin

# Register your models here.
from .models import Operation, Securities

admin.site.register(Operation)
admin.site.register(Securities)

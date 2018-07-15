from django.contrib import admin

from .models import UserProfile, Country

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Country)

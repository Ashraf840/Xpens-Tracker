from django.contrib import admin
from .models import UserPreference

# Register your models here.
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency']
    search_fields = ['currency']
    list_per_page = 8

admin.site.register(UserPreference, UserPreferenceAdmin)

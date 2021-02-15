from django.contrib import admin
from .models import Income


# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'category', 'date', 'description', 'amount']
    search_fields = ['owner', 'date', 'category', 'description']
    list_per_page = 8

admin.site.register(Income, IncomeAdmin)
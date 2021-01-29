from django.contrib import admin
from .models import Expense, Category


# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'description', 'amount']
    search_fields = ['owner', 'date', 'description']
    list_per_page = 8

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 8


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
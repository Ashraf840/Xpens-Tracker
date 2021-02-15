from django.contrib import admin
from .models import Expense, Category


# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'category', 'date', 'description', 'amount']
    search_fields = ['owner', 'date', 'category', 'description']
    list_per_page = 8

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'categorytype', 'owner']
    list_filter = ['categorytype']
    search_fields = ['name', 'categorytype']
    list_per_page = 8


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
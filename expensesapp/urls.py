from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'expensesApp'

urlpatterns = [
    path('', views.index, name='home'),
    path('expense-list/', views.expenseList, name='addExpense'),
    path('search-expense/', csrf_exempt(views.search_expenses), name='search_expense'),
    path('add-expense/', views.addExpense, name='createNewExpense'),
    path('update-expense/<int:id>/', views.updateExpense, name='updateExpense'),
    path('delete-expense/<int:id>/', views.deleteExpense, name='deleteExpense'),
    
    path('category-list/', views.categoryList, name='categorylist'),
    path('add-category/', views.addCategory, name='createNewCategory'),
    path('update-category/<int:id>/', views.updateCategory, name='updateCategory'),
    path('delete-category/<int:id>/', views.deleteCategory, name='deleteCategory'),
]
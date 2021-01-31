from django.urls import path
from . import views

app_name = 'expensesApp'

urlpatterns = [
    path('', views.index, name='home'),
    path('expense-list/', views.expenseList, name='addExpense'),
    path('add-expense/', views.addExpense, name='createNewExpense'),
    path('update-expense/<int:id>/', views.updateExpense, name='updateExpense'),
    path('delete-expense/<int:id>/', views.deleteExpense, name='deleteExpense'),
    
    path('category-list/', views.categoryList, name='categorylist'),
    path('add-category/', views.addCategory, name='createNewCategory'),
    path('update-category/<int:id>/', views.updateCategory, name='updateCategory'),
]
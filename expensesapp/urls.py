from django.urls import path
from . import views

app_name = 'expensesApp'

urlpatterns = [
    path('', views.index, name='home'),
    path('add-expense/', views.addExpense, name='addExpense'),
]
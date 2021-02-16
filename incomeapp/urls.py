from django.urls import path
from . import views
# from django.views.decorators.csrf import csrf_exempt

app_name = 'incomeApp'

urlpatterns = [
    path('income-list/', views.incomeList, name='incomeList'),
    path('add-income/', views.addIncome, name='createNewIncome'),
    path('update-income/<int:id>/', views.updateIncome, name='updateIncome'),
    path('delete-income/<int:id>/', views.deleteIncome, name='deleteIncome'),
]
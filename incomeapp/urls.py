from django.urls import path
from . import views
# from django.views.decorators.csrf import csrf_exempt

app_name = 'incomeApp'

urlpatterns = [
    path('income-list/', views.incomeList, name='incomeList'),
]
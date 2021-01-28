from django.urls import path
from . import views

app_name = 'userpreferencesApp'

urlpatterns = [
    path('', views.index, name='settings'),
]
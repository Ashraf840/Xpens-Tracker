from django.urls import path
from . import views

app_name = "authenticationApp"

urlpatterns = [
    path('register/', views.userRegistration, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
]
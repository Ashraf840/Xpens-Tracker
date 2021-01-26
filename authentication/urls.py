from django.urls import path
from . import views

app_name = "authenticationApp"

urlpatterns = [
    path('register/', views.userRegistration, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),

    path('validate-username/', views.usernameValidation, name='validate_username'),
    path('validate-email/', views.emailValidation, name='validate_email'),

    # User Account Activation
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),      # the name 'activate' is used in the 'link' variable of 'activate_url'
]
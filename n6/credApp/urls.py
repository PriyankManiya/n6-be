from django.urls import path, include
from . import views

# A list of url patterns.
urlpatterns = [
    path('', views.CredApiView.as_view(), name='cred'),
    path('list/', views.CredListApiView.as_view(), name='cred-list'),
    path('login/', views.UserLoginView.as_view(), name='cred-login'),
    path('register/', views.UserRegistrationView.as_view(), name='cred-register'),
    path('profile/', views.CredApiView.as_view(), name='cred-profile'),
    path('changepassword/', views.UserChangePasswordView.as_view(), name='cred-change-password'),
    path('send-reset-password/', views.SendEmailView.as_view(), name='cred-send-reset-password'),
    path('reset-password/<cid>/<token>/', views.ResetPasswordView.as_view(), name='cred-reset-password'),
]

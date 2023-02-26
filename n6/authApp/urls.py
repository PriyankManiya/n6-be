from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('company/', views.CompanyRegistrationView.as_view(), name='company'),
    # path('login/', views.UserLoginView.as_view(), name='login'),
    # path('profile/', views.UserProfileView.as_view(), name='profile'),
    # path('users-list/', views.UsersList.as_view(), name='users-list'),
    # path('changepassword/', views.UserChangePasswordView.as_view(), name='changepassword'),
    # path('send-reset-password/', views.SendEmailView.as_view(), name='send-reset-password'),
    # path('reset-password/<uid>/<token>/', views.ResetPasswordView.as_view(), name='reset-password'),
]
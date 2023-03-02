from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CredApiView.as_view(), name='cred'),
    path('list/', views.CredListApiView.as_view(), name='cred-list'),
    path('login/', views.UserLoginView.as_view(), name='cred-login'),
    path('register/', views.UserRegistrationView.as_view(), name='cred-register'),
    path('profile/', views.CredApiView.as_view(), name='cred-profile'),
]

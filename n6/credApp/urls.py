from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CredApiView.as_view(), name='cred'),
    path('list/', views.CredListApiView.as_view(), name='cred'),
]

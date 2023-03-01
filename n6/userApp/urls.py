from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.UserApiView.as_view(), name='user'),
    path('list/', views.UserListApiView.as_view(), name='user-list'),
]

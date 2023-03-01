from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CompanyApiView.as_view(), name='company'),
    path('list/', views.CompanyListApiView.as_view(), name='company-list'),
]

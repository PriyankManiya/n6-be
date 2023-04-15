from django.urls import path, include
from . import views

# Creating a url pattern for the company api view.
urlpatterns = [
    path('', views.CompanyApiView.as_view(), name='company'),
    path('list/', views.CompanyListApiView.as_view(), name='company-list'),
]

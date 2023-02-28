from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CompanyRegistrationView.as_view(), name='company'),
]

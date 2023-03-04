from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AttachmentApiView.as_view(), name='attachment'),
]

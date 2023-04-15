from django.urls import path, include
from . import views

# A list of url patterns.
urlpatterns = [
    path('', views.AttachmentApiView.as_view(), name='attachment'),
]

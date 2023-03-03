from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProjectApiView.as_view(), name='project'),
    path('list/', views.ProjectListApiView.as_view(), name='project-list'),
]

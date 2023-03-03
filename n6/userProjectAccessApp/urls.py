from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProjectAccessApiView.as_view(), name='user-project-access'),
    path('list/', views.UserProjectAccessListApiView.as_view(), name='user-project-access-list'),
]

from django.urls import path
from . import views

# Creating a list of urls that will be used by the app.
urlpatterns = [
    path('', views.UserProjectAccessApiView.as_view(), name='user-project-access'),
    path('list/', views.UserProjectAccessListApiView.as_view(), name='user-project-access-list'),
]

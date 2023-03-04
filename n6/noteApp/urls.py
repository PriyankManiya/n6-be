from django.urls import path
from . import views

urlpatterns = [
    # path('', views.NoteApiView.as_view(), name='note'),
    path('list/', views.NoteListApiView.as_view(), name='note-list'),
]

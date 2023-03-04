from django.urls import path
from . import views

urlpatterns = [
    path('note/', views.NoteApiView.as_view(), name='note'),
    path('respond/', views.RespondNoteApiView.as_view(), name='note-respond'),
    path('list/', views.NoteListApiView.as_view(), name='note-list'),
]

from django.urls import path
from . import views

# A list of paths that are used to access the views.
urlpatterns = [
    path('', views.NoteApiView.as_view(), name='note'),
    path('read/', views.NoteReadApiView.as_view(), name='note-read'),
    path('respond/<id>', views.RespondNoteApiView.as_view(), name='note-respond'),
    path('list/<id>', views.NoteListApiView.as_view(), name='note-list'),
]

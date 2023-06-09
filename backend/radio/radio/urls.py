from django.urls import path
from music.views import create_user, add_audio, download_audio

urlpatterns = [
    path('api/create_user/', create_user, name='create_user'),
    path('api/add_audio/', add_audio, name='add_audio'),
    path('record/', download_audio, name='download_audio'),
]

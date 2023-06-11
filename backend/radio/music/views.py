import os
import uuid

import ffmpeg
from django.http import FileResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Audio, User


@api_view(['POST'])
def create_user(request):
    name = request.data.get('name')
    if name:
        access_token = str(uuid.uuid4())
        user = User.objects.create(name=name, access_token=access_token)
        return Response({'user_id': user.user_id, 'access_token': user.access_token})
    else:
        return Response({'error': 'Name parameter is missing.'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_audio(request):
    user_id = request.data.get('user_id')
    access_token = request.data.get('access_token')
    audio_file = request.FILES.get('audio_file')

    if not user_id or not access_token or not audio_file:
        return Response({'error': 'Missing parameters.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(user_id=user_id, access_token=access_token)
    except User.DoesNotExist:
        return Response({'error': 'Invalid user credentials.'},
                        status=status.HTTP_401_UNAUTHORIZED)
    audio_id = str(uuid.uuid4())
    audio_path = os.path.join('media', 'audio', f'{audio_id}.mp3')
    try:
        stream = ffmpeg.input(audio_file.temporary_file_path())
        stream = ffmpeg.output(stream, audio_path)
        ffmpeg.run(stream)
    except (ffmpeg.Error, FileNotFoundError):
        return Response({'error': 'Audio conversion failed.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    audio = Audio.objects.create(user=user, audio_id=audio_id)
    download_url = request.build_absolute_uri(
        reverse('download_audio') + f'?id={audio_id}&user={user_id}')
    return Response({'download_url': download_url})


@api_view(['GET'])
def download_audio(request):
    audio_id = request.GET.get('id')
    user_id = request.GET.get('user')
    if not audio_id or not user_id:
        return Response({'error': 'Missing parameters.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Invalid user credentials.'},
                        status=status.HTTP_401_UNAUTHORIZED)
    try:
        audio = Audio.objects.get(audio_id=audio_id, user=user)
    except Audio.DoesNotExist:
        return Response({'error': 'Audio not found.'},
                        status=status.HTTP_404_NOT_FOUND)
    audio_path = os.path.join('media', 'audio', f'{audio_id}.mp3')
    response = FileResponse(open(audio_path, 'rb'), content_type='audio/mpeg')
    return response

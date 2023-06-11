import os
import uuid
from django.http import FileResponse
import ffmpeg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse

from .models import User, Audio


@api_view(['POST'])
def create_user(request):
    name = request.data.get('name')
    if name:
        access_token = str(uuid.uuid4())
        user = User.objects.create(name=name, access_token=access_token)
        return Response({'user_id': user.user_id, 'access_token': user.access_token})
    else:
        return Response({'error': 'Name parameter is missing.'}, status=400)


@api_view(['POST'])
def add_audio(request):
    user_id = request.data.get('user_id')
    access_token = request.data.get('access_token')
    audio_file = request.FILES.get('audio_file')

    if not user_id or not access_token or not audio_file:
        return Response({'error': 'Missing parameters.'}, status=400)

    # Проверяем наличие пользователя в базе данных
    try:
        user = User.objects.get(user_id=user_id, access_token=access_token)
    except User.DoesNotExist:
        return Response({'error': 'Invalid user credentials.'}, status=401)

    # Генерируем уникальный идентификатор и путь для сохранения аудиозаписи
    audio_id = str(uuid.uuid4())
    audio_path = os.path.join('media', 'audio', f'{audio_id}.mp3')

    # Преобразуем аудиозапись в формат mp3 с помощью ffmpeg
    try:
        stream = ffmpeg.input(audio_file.temporary_file_path())
        stream = ffmpeg.output(stream, audio_path)
        ffmpeg.run(stream)
    except (ffmpeg.Error, FileNotFoundError):
        return Response({'error': 'Audio conversion failed.'}, status=500)

    # Сохраняем информацию об аудиозаписи в базе данных
    audio = Audio.objects.create(user=user, audio_id=audio_id)

    # Возвращаем URL для скачивания записи
    download_url = request.build_absolute_uri(reverse('download_audio') + f'?id={audio_id}&user={user_id}')
    return Response({'download_url': download_url})


@api_view(['GET'])
def download_audio(request):
    audio_id = request.GET.get('id')
    user_id = request.GET.get('user')

    if not audio_id or not user_id:
        return Response({'error': 'Missing parameters.'}, status=400)

    # Проверяем наличие пользователя в базе данных
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Invalid user credentials.'}, status=401)

    # Проверяем наличие аудиозаписи в базе данных
    try:
        audio = Audio.objects.get(audio_id=audio_id, user=user)
    except Audio.DoesNotExist:
        return Response({'error': 'Audio not found.'}, status=404)

    # Получаем путь к файлу аудиозаписи
    audio_path = os.path.join('media', 'audio', f'{audio_id}.mp3')

    # Возвращаем аудиозапись в виде HTTP-ответа
    response = FileResponse(open(audio_path, 'rb'), content_type='audio/mpeg')
    return response

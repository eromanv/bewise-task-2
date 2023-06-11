import os

import django
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from rest_framework.test import APIClient
from django.urls import reverse
from music.models import Audio, User
from rest_framework import status

django.setup()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create(name='Test User', access_token='test_token')


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.mkdir('media')


@pytest.mark.django_db
def test_create_user(client):
    url = reverse('create_user')
    data = {'name': 'New User'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'user_id' in response.data
    assert 'access_token' in response.data


def test_create_user_missing_name(client):
    url = reverse('create_user')
    response = client.post(url, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data


def test_add_audio_missing_parameters(client):
    url = reverse('add_audio')
    response = client.post(url, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data


def test_download_audio_missing_parameters(client):
    url = reverse('download_audio')
    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data

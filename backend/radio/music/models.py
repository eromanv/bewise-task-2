from django.db import models
import uuid


class User(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    access_token = models.CharField(max_length=255)


class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_id = models.UUIDField(default=uuid.uuid4, editable=False)

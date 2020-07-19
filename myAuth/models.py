from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from datetime import datetime

# Create your models here.

class UserUUID(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField()

class Texts(models.Model):
    user_uuid = models.ForeignKey(
        UserUUID,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=40)
    text = models.TextField()
    date = models.DateField(default=datetime.now())
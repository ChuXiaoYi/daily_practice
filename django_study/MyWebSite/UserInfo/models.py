from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    img = models.ImageField(upload_to='img')
    nickname = models.CharField(max_length=10, default='user')
    skill = models.CharField(max_length=20, blank=True)
    introduction = models.CharField(max_length=100, blank=True)

    class Meta(AbstractUser.Meta):
        pass

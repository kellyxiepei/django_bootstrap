from django.db import models


class User(models.Model):
    credential = models.CharField(max_length=128, db_index=True, unique=True, null=False)
    secret = models.CharField(max_length=128, null=True)
    nickname = models.CharField(max_length=128)
    avatar = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

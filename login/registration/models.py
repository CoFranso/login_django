from django.db import models
from django.contrib.auth.models import User

import uuid


# Create your models here.

class EmailChange(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    new_email = models.EmailField(max_length=100, blank=False, null=False)
    expiration_time = models.DateTimeField()

    @classmethod
    def save_token(cls, user, new_email, expiration_time):
        email_change = cls.objects.create(user=user, new_email=new_email, expiration_time=expiration_time)
        return email_change

    @classmethod
    def get_token(cls, token):
        try:
            return cls.objects.get(token=token)
        except cls.DoesNotExist:
            return None

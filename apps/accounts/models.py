from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=13, unique=True)
    bio = models.TextField(blank=True, null=True)
    telegram_id = models.CharField(max_length=64, blank=True, null=True)
    chat_id = models.CharField(max_length=64, blank=True, null=True)
    telegram_username = models.CharField(max_length=64, blank=True, null=True)
    image = models.ImageField(upload_to='accounts/%Y/%m/%d/', null=True, blank=True)

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return ''
    
    @property
    def has_telegram(self) -> bool:
        return bool(self.telegram_id)

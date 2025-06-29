# accounts/models.py
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # 使用 OneToOneField 將 Profile 與 User 連結起來
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=100)
    owner_address = models.CharField(max_length=255, blank=True)  # 地址可選填

    def __str__(self):
        return self.owner_name
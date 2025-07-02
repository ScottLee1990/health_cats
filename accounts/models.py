# accounts/models.py
# 先用Django內建的User模型頂著

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # OneToOneField連接User模型
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=100)
    owner_address = models.CharField(max_length=255, blank=True)
    # 待擴充

    def __str__(self):
        return self.owner_name
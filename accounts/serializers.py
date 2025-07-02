# accounts/serializers.py

from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # 先把user欄位設為唯讀,考慮看看要不要直接用username做資料
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'owner_name', 'owner_address']
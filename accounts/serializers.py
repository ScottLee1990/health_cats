# accounts/serializers.py

from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # 讓 `user` 欄位在讀取時顯示使用者名稱，且設為唯讀
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'owner_name', 'owner_address']
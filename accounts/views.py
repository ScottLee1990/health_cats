# accounts/views.py

from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    提供當前登入使用者的 Profile 讀取與更新功能。
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # 權限：必須登入

    def get_object(self):
        """
        改寫這個方法，永遠只回傳與當前登入使用者關聯的 Profile 物件。
        """
        # 嘗試取得 Profile，如果不存在就為該使用者建立一個空的 Profile
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        return obj
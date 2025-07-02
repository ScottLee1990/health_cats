# accounts/views.py

from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateAPIView):

    # Profile的讀寫功能

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # 權限：須登入

    def get_object(self):

        # 嘗試取得Profile，如果不存在就create new Profile
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        return obj
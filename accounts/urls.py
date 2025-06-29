# accounts/urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ProfileDetailView

urlpatterns = [
    # 當有 POST 請求送到這個 URL 時，由 obtain_auth_token 視圖處理
    path('login/', obtain_auth_token, name='api-login'),
    path('profile/', ProfileDetailView.as_view(), name='api-profile'),
]
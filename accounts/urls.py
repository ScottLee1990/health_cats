# accounts/urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ProfileDetailView

urlpatterns = [
    # obtain_auth_token負責處理POST
    path('login/', obtain_auth_token, name='api-login'),
    path('profile/', ProfileDetailView.as_view(), name='api-profile'),
]
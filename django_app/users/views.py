from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """用户注册视图"""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class UserDetailView(generics.RetrieveAPIView):
    """获取用户详情"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义令牌获取视图"""

    serializer_class = CustomTokenObtainPairSerializer

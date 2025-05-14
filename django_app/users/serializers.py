from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    '''用户序列化器'''

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')
        read_only_fields = ('date_joined',)


class RegisterSerializer(serializers.ModelSerializer):
    '''注册序列化器'''
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        '''验证两次密码是否一致'''
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码不匹配"})
        return attrs

    def create(self, validated_data):
        '''创建用户'''
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''自定义令牌序列化器，添加用户信息'''

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

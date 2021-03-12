from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic', 'bio', 'location', 'birth_date']


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic', 'bio', 'location', 'birth_date']


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Profile


class ProfileDetailSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'follows']


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class UserUpdateSerializer(ModelSerializer):
    profile = ProfileDetailSerializer()

    def update(self, instance, validated_data):
        if validated_data.get('username'):
            instance.username = validated_data['username']
            instance.save()
        if validated_data.get('profile'):
            if validated_data.get('profile').get('bio'):
                instance.profile.bio = validated_data['profile']['bio']
            if validated_data.get('profile').get('profile_pic'):
                instance.profile.profile_pic = validated_data['profile']['profile_pic']
        instance.profile.save()
        return instance

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']


class UserDetailSerializer(ModelSerializer):
    profile = ProfileDetailSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

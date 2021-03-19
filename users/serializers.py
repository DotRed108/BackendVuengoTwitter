from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic', 'bio']


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic', 'bio', 'following', 'followers', 'post_set', 'bookmarks']


class UserLimitedDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'profile_pic', 'username']


class UserCreateSerializer(ModelSerializer):

    password2 = CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(username=self.validated_data['username'],
                    email=self.validated_data['email'],
                    )
        password = self.validated_data['password']
        password2 = self.validated_data['password']

        if password != password2:
            raise ValidationError({'password': 'Passwords do not match'})
        user.set_password(password)
        user.save()
        return user

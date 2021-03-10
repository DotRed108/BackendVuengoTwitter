from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import UserDetailSerializer, UserUpdateSerializer
from .permissions import CanDeleteUser, CanUpdateUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [CanUpdateUser]
        elif self.action == 'delete':
            self.permission_classes = [CanDeleteUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        else:
            return UserDetailSerializer

    @action(["POST"], detail=True)
    def follow(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, id=kwargs.get('pk'))
        target_user.followers.add(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(["POST"], detail=True)
    def unfollow(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, id=kwargs.get('pk'))
        if len(target_user.followers.filter(id=request.user.id)) != 0:
            target_user.followers.remove(request.user)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_201_CREATED)

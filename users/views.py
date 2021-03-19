from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import UserDetailSerializer, UserUpdateSerializer, UserCreateSerializer
from .permissions import CanDeleteUser, CanUpdateUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view
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
        elif self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        elif self.action == 'create':
            return UserCreateSerializer
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


@api_view(['GET'])
def get_logged_in_user(request):
    if request.method == 'GET':
        return Response({'userId': request.user.id}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import UserDetailSerializer, UserUpdateSerializer, UserCreateSerializer, UserSerializer
from .permissions import CanDeleteUser, CanUpdateUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


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
        target_user.followers.remove(request.user)
        return Response(status=status.HTTP_201_CREATED)


def serialize_profile_data(target_user, request):
    serializer = UserDetailSerializer(target_user)
    response_data = serializer.data
    if request.user.id in serializer.data['followers']:
        response_data['isFollowing'] = 'true'
    else:
        response_data['isFollowing'] = 'false'
    response_data['followers'] = len(serializer.data['followers'])
    response_data['following'] = len(serializer.data['following'])
    return response_data


@api_view(['GET'])
def get_logged_in_user(request):
    if request.method == 'GET':
        return Response({'userId': request.user.id}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_random_profile(request):
    if request.method == 'GET':
        query_set = User.objects.all().order_by('?')
        target_user = query_set[0]
        response_data = serialize_profile_data(target_user, request)
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_profile(request, pk):
    if request.method == 'GET':
        target_user = get_object_or_404(User, pk=pk)
        response_data = serialize_profile_data(target_user, request)
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def follower_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user_set = paginator.paginate_queryset(user.followers.all(), request)
        serializers = UserSerializer(user_set, many=True)
        return paginator.get_paginated_response(serializers.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def following_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user_set = paginator.paginate_queryset(user.following.all(), request)
        serializers = UserSerializer(user_set, many=True)
        return paginator.get_paginated_response(serializers.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
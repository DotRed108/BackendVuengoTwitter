from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post
from django.middleware.csrf import get_token
from django.http.response import JsonResponse
from rest_framework.response import Response
from main.serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from users.serializers import UserSerializer, UserLimitedDetailSerializer
from rest_framework.pagination import PageNumberPagination


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token})


def serialize_posts_with_user_data(query_set, request):
    paginator = PageNumberPagination()
    # This is where the actual pagination occurs
    paginator.page_size = 10
    post_set = paginator.paginate_queryset(query_set, request)
    author_list = []
    for item in post_set:
        author_list.append(item.author)
    serializer1 = UserLimitedDetailSerializer(author_list, many=True)
    serializer = PostSerializer(post_set, many=True)
    i = 0
    while i < len(serializer.data):
        serializer.data[i]['username'] = serializer1.data[i]['username']
        serializer.data[i]['profile_pic'] = serializer1.data[i]['profile_pic']
        i = i + 1
    for post in serializer.data:
        if request.user.id in post['likes']:
            post['hasLiked'] = 'true'
        else:
            post['hasLiked'] = 'false'
        post['likes'] = len(post['likes'])
    return serializer


@api_view(['GET'])
def home_post_list(request):
    if request.method == 'GET':
        query_set = Post.objects.filter(
            Q(author=request.user) | Q(author__in=request.user.following.all())
        ).filter(parent_post__isnull=True).order_by('-date_posted')
        # this is a hacky way of getting the get paginated response function to work with my custom serialized data
        paginator = PageNumberPagination()
        paginator.page_size = 1
        paginator.paginate_queryset(query_set, request)
        serializer = serialize_posts_with_user_data(query_set, request)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_posts(request):
    if request.method == 'GET':
        query_set = Post.objects.all()
        paginator = PageNumberPagination()
        post_set = paginator.paginate_queryset(query_set, request)
        serializer = PostSerializer(post_set, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_post_list(request, pk):
    if request.method == 'GET':
        query_set = Post.objects.filter(Q(author=pk) & Q(parent_post__isnull=True)).order_by('-date_posted')
        paginator = PageNumberPagination()
        paginator.page_size = 1
        paginator.paginate_queryset(query_set, request)
        serializer = serialize_posts_with_user_data(query_set, request)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_post_list(request, content):
    if request.method == 'GET':
        query_set = Post.objects.filter(content__icontains=content)
        paginator = PageNumberPagination()
        paginator.page_size = 1
        paginator.paginate_queryset(query_set, request)
        serializer = serialize_posts_with_user_data(query_set, request)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        context = {
            'request': request,
        }
        serializer = PostCreateSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detail_post(request, pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=pk)
        query_set = Post.objects.filter(Q(parent_post=post.id) | Q(id=post.id)).order_by('date_posted')
        paginator = PageNumberPagination()
        paginator.page_size = 1
        paginator.paginate_queryset(query_set, request)
        serializer = serialize_posts_with_user_data(query_set, request)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'PUT' and post.author == request.user:
        serializer = PostUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'DELETE' and post.author == request.user:
        post.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.likes.add(request.user)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.likes.remove(request.user)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def like_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user_set = paginator.paginate_queryset(post.likes.all(), request)
        serializers = UserSerializer(user_set, many=True)
        return paginator.get_paginated_response(serializers.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def bookmark_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    query_set = Post.objects.filter(bookmarked=request.user)
    if request.method == 'POST':
        if post not in query_set:
            post.bookmarked.add(request.user)
        else:
            post.bookmarked.remove(request.user)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def bookmarks_list(request):
    if request.method == 'GET':
        query_set = Post.objects.filter(bookmarked=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 1
        paginator.paginate_queryset(query_set, request)
        serializer = serialize_posts_with_user_data(query_set, request)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_bookmark_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.bookmarked.remove(request.user)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

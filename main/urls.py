from django.urls import path
from .views import home_post_list,  create_post, detail_post, delete_post, update_post, like_post, unlike_post,\
    like_list, user_post_list, search_post_list, bookmarks_list, bookmark_post, remove_bookmark_post, all_posts

urlpatterns = [
    path('api/home/', home_post_list, name="home"),
    path('api/create-post/', create_post, name="create-post"),
    path('api/detail-post/<int:pk>/', detail_post, name="post-detail"),
    path('api/update-post/<int:pk>/', update_post, name="update-post"),
    path('api/delete-post/<int:pk>/', delete_post, name="delete-post"),
    path('api/like-post/<int:pk>/', like_post, name="like-post"),
    path('api/unlike-post/<int:pk>/', unlike_post, name="unlike-post"),
    path('api/like-list/<int:pk>/', like_list, name="like-list"),
    path('api/user-post-list/<int:pk>/', user_post_list, name="user-post-list"),
    path('api/search-post/<str:content>/', search_post_list, name="search-post-list"),
    path('api/bookmark-list/', bookmarks_list, name="bookmark-list"),
    path('api/bookmark-post/<int:pk>/', bookmark_post, name="bookmark-post"),
    path('api/remove-bookmark-post/<int:pk>/', remove_bookmark_post, name="remove-bookmark-post"),
    path('api/all-posts/', all_posts, name="all-posts-list"),
]

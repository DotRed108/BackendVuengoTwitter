from django.urls import path
from .views import home_post_list,  create_post, detail_post, delete_post, update_post, like_post, unlike_post,\
    like_list

urlpatterns = [
    path('api/home/', home_post_list, name="home"),
    path('api/create-post/', create_post, name="create-post"),
    path('api/detail-post/<int:pk>', detail_post, name="post-detail"),
    path('api/update-post/<int:pk>', update_post, name="update-post"),
    path('api/delete-post/<int:pk>', delete_post, name="delete-post"),
    path('api/like-post/<int:pk>', like_post, name="like-post"),
    path('api/unlike-post/<int:pk>', unlike_post, name="unlike-post"),
    path('api/like-list/<int:pk>', like_list, name="like-list")
]

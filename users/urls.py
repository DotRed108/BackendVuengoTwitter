from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, get_logged_in_user, get_profile, following_list, follower_list

router = DefaultRouter()
router.register('api/user', UserViewSet, basename="users")

urlpatterns = [
    path('api/user/get-logged-in-user/', get_logged_in_user, name="get logged in user"),
    path('api/user/get-profile/<int:pk>/', get_profile, name="get profile"),
    path('api/user/<int:pk>/followers/', follower_list, name="get followers"),
    path('api/user/<int:pk>/following/', following_list, name="get followers"),
]

urlpatterns += router.urls

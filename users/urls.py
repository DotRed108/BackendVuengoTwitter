from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, get_logged_in_user

router = DefaultRouter()
router.register('api/user', UserViewSet, basename="users")

urlpatterns = [
    path('api/user/get-logged-in-user/', get_logged_in_user, name="get logged in user")
]

urlpatterns += router.urls

from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register('api/user', UserViewSet, basename="users")

urlpatterns = [
]

urlpatterns += router.urls

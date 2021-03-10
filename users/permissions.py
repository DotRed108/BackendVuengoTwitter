from rest_framework.permissions import IsAuthenticated


class CanUpdateUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        else:
            return False


class CanDeleteUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        else:
            return False

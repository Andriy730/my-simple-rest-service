from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the advertisement.
        return obj.owner == request.user

class IsTheSameUserOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow user edit user's data"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True

        #Write permissions are only allowed to the user himself.
        return obj.id == request.user.id

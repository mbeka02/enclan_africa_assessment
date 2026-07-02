from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow read access to anyone, but restrict writes to the post's author."""

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS are always permitted
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

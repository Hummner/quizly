from rest_framework.permissions import BasePermission

class IsQuizOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user
        owner = obj.owner

        return user == owner
from rest_framework.permissions import BasePermission


class IsQuizOwner(BasePermission):
    """
    Object-level permission.

    Allows access only if the requesting user
    is the owner of the quiz object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks whether the current user
        matches the object's owner.
        """

        user = request.user
        owner = obj.owner

        return user == owner

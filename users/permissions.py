from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Allows access only to users who are in the Moderators group.
    """

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Moderators").exists()

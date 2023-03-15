from rest_framework import permissions
from .constants import (
                supervisor,
                hod,
                cto,
                president,
                ceo,
                analyst
                )


class IsAuthorizeUserPermissionOnly(permissions.DjangoModelPermissions):
    """This permission only allow the user if they are not analyst position"""

    approve_levels = [supervisor.name, cto.name, hod.name, president.name, ceo.name]

    def has_permission(self, request, view):
        """Return true for user whose level is among the approve_levels, otherwise return False"""
        level = request.user.level.name.lower().strip()
        # if level not in self.approve_levels:
        #     return False
        # return True
        return level in self.approve_levels

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsAuthorizeToRaiseIssue(permissions.DjangoModelPermissions):
    """If user has not been assigned a department and level, do not allow them to create a ticket.
    Only user who has level and department can raise a ticket issue.
    """

    def has_permission(self, request, view):
        user = request.user
        return user.level and user.department
        # if user.level and user.department:
        #     return True
        # return False


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        # if obj.user == user:
        #     return True
        # return False
        return obj.user == user


class IsPermittedToMakeDecision(permissions.BasePermission):

    message = 'You do not have to access this ticket, either you don\'t have the permission or the ticket has not been publish'

    def has_object_permission(self, request, view, obj):
        user = request.user
        level = user.level.name.strip().lower()
        depratment = user.department 

        if user.is_superuser:
            return True
        
        if obj.publish:

            if level == supervisor.name and depratment == obj.department and obj.user.level.name.strip().lower() == analyst.name:
                return True

            if level == hod.name and depratment == obj.department and obj.user.level.name.strip().lower() == supervisor.name:
                return True

            if level == cto.name and obj.user.level.name.strip().lower() == hod.name:
                return True

            if level == president.name and obj.user.level.name.strip().lower() == cto.name:
                return True 

            if level == ceo.name and obj.user.level.name.strip().lower() == president.name:
                return True

            return False
        return False
from rest_framework import permissions


class IsAuthorizeUserPermissionOnly(permissions.DjangoModelPermissions):
    """This permission only allow the user if they are not analyst position"""

    approve_levels = ['supervisor', 'cto/cfo', 'head of department', 'president', 'ceo']

    def has_permission(self, request, view):
        """Return true for user whose level is among the approve_levels, otherwise return False"""
        level = request.user.level.name.lower().strip()
        if level not in self.approve_levels:
            return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsAuthorizeToRaiseIssue(permissions.DjangoModelPermissions):
    """If user has not been assigned a department and level, do not allow them to create a ticket.
    Only user who has level and department can raise a ticket issue.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.level and user.department:
            return True
        return False


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class IsPermittedToMakeDecision(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        level = user.level.name.strip().lower()
        depratment = user.department 

        if user.is_superuser:
            return True

        if level == 'supervisor' and depratment == obj.department and obj.user.level.name.strip().lower() == 'analyst':
            return True

        if level == 'head of department' and depratment == obj.department and obj.user.level.name.strip().lower() == 'supervisor':
            return True

        if level == 'cto/cfo' and obj.user.level.name.strip().lower() == 'head of department':
            return True

        if level == 'president' and obj.user.level.name.strip().lower() == 'cto/cfo':
            return True 

        if level == 'ceo' and obj.user.level.name.strip().lower() == 'president':
            return True

        return False
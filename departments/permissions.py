from rest_framework import permissions


class IsAdminApproveUserOnly(permissions.DjangoModelPermissions):
    """This permission only allow the user if they are not analyst position"""

    approve_levels = ['supervisor', 'head of department']

    def has_permission(self, request, view):
        """Return true for user whose level is among the approve_levels and in Administrative department, otherwise return False"""
        level = request.user.level.name.lower()
        department = request.user.department.name.lower()

        if level not in self.approve_levels:
            return False

        if department != "administrative department":
            return False 

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


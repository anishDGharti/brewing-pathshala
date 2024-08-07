from rest_framework.permissions import BasePermission


class DynamicPermission(BasePermission):
    def has_permission(self, request, view):
        required_permissions = getattr(view, "required_permissions", [])
        print("Required permissions:", required_permissions)

        if request.user.is_superuser:
            return True
        if not request.user or not request.user.is_authenticated:
            print("User is not authenticated")
            return False

        # Check individual user permissions
        user_permissions = request.user.user_permissions.values_list(
            "codename", flat=True
        )
        print("User permissions:", user_permissions)

        if any(perm in user_permissions for perm in required_permissions):
            print("Permission granted by specific user permission")
            return True

        # Check group permissions
        user_groups = request.user.groups.all()
        print("User groups:", user_groups)

        for group in user_groups:
            group_permissions = group.permissions.values_list("codename", flat=True)
            print(f"Permissions for group {group}: {group_permissions}")

            if any(
                permission in group_permissions for permission in required_permissions
            ):
                print("Permission granted by group")
                return True

        print("Permission denied by both checks")
        return False


class DynamicPermissionMixin:
    required_permissions = []

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = self.permission_classes[:]  # Copy any default permissions
        if self.required_permissions:
            permission_classes.append(DynamicPermission)
        return [permission() for permission in permission_classes]
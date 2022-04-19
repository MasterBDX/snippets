from django.core.exceptions import PermissionDenied


class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_admin or user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()

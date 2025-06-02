from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

#Mixin para proteger las vistas de administrador (da por hecho que el usuario está registrado)
class UserTypeRequiredMixin(LoginRequiredMixin):
    required_user_type = None 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.required_user_type and getattr(request.user, 'user_type', None) != self.required_user_type:
            messages.warning(request, "No tienes permisos para acceder al panel de administración")
            return redirect('landpage')

        return super().dispatch(request, *args, **kwargs)

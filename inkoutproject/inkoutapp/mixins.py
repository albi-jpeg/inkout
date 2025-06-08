from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from functools import wraps

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

class UsuarioOnlyMixin(UserTypeRequiredMixin):
    required_user_type = 'usuario'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type != self.required_user_type:
            messages.warning(request, "Solo los usuarios pueden pedir citas.")
            return redirect('perfil')

        return super().dispatch(request, *args, **kwargs)
    

def artista_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('perfil')

        if request.user.user_type != 'artista':
            messages.error(request, "No tienes permiso para acceder aquí.")
            return redirect('perfil')

        return view_func(request, *args, **kwargs)
    return _wrapped_view
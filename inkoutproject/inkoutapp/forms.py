# forms.py
from django import forms
from .models import Artista, MyUser, Cita, Disenyo, Promocion
from django.contrib.auth.forms import UserCreationForm


class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['usuario', 'nombre_artistico', 'foto_perfil', 'biografia', 'sitio_web']

    
    
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['nombre', 'email', 'user_type', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  
        if commit:
            user.save()
        return user


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['artista', 'usuario', 'fecha', 'hora', 'estado']

class DisenyoForm(forms.ModelForm):
    class Meta:
        model = Disenyo
        fields = ['artista', 'titulo', 'descripcion', 'imagen']

class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['titulo', 'descripcion', 'fecha_fin', 'codigo_qr']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['nombre', 'email', 'foto_perfil']
        

class RegistroUsuarioForm(UserCreationForm):
    nombre = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ('nombre', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.email = self.cleaned_data['email']
        user.user_type = 'usuario'  # Por defecto, user_type usuario
        if commit:
            user.save()
        return user

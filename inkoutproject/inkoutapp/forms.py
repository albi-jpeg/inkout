# forms.py
from django import forms
from .models import Artista, MyUser, Cita, Disenyo, Promocion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser

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
        

# forms.py
from django import forms
from .models import MyUser

class RegistroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('nombre', 'email')  

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_type = 'usuario'
        if commit:
            user.save()
        return user

"""
URL configuration for inkoutproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inkoutapp.views import *
from usuarios.views import *
from login.views import *
from django.contrib.auth.views import LogoutView
from adminapp.views import AdminPanelView
from django.contrib.auth import views as auth_views


urlpatterns = [
    #URL's de las vistas normales
    path('admin', AdminPanelView.as_view(), name='admin'),
    path('', LandpageView.as_view(), name='landpage'),
    path('login', LoginFormView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='landpage'), name='logout'), 
    path('registro/', RegistroView.as_view(), name='registro'),
    path('artista/<int:pk>', ArtistaView.as_view(), name='artista'),
    path('disenyo/<int:pk>', DisenyoView.as_view(), name='disenyo'),
    path('error', ErrorView.as_view(), name='error'),
    path('perfil', PerfilView.as_view(), name='perfil'),
    path('promocion/<int:pk>', PromoView.as_view(), name='promocion'),
    path('promociones', PromocionesView.as_view(), name='promociones'),
    path('pedircita', PedirCitaView.as_view(), name='pedircita'),
    path('contacto', ContactoView.as_view(), name='form_contacto'),
    path('cookies', CookiesView.as_view(), name='cookies'),
    path('privacidad', PrivView.as_view(), name='privacidad'),
    path('terminos_y_condiciones', TeryconView.as_view(), name='terminos_y_condiciones'),

    
    #URL's del administrador
    path('admin/artistas', artista_mostrar, name='artista_mostrar'),
    path('admin/artistas/crear', artista_crear, name='artista_crear'),

    path('admin/citas', cita_mostrar, name='cita_mostrar'),
    path('admin/citas/crear', cita_crear, name='cita_crear'),

    
    path('admin/disenyos', disenyo_mostrar, name='disenyo_mostrar'),
    path('admin/disenyos/crear', disenyo_crear, name='disenyo_crear'),
    
    path('admin/promos', promo_mostrar, name='promo_mostrar'),
    path('admin/promos/crear', promo_crear, name='promo_crear'),

    path('admin/usuarios', usuario_mostrar, name='usuario_mostrar'),
    path('admin/usuarios/crear', usuario_crear, name='usuario_crear'),
    
    path('admin/mensajes', mensaje_mostrar, name='mensaje_mostrar'),
    
    path('mis-disenyos/', mis_disenyos, name='mis_disenyos'),
    path('mis-disenyos/crear/', mis_disenyos_crear, name='mis_disenyos_crear'),
    path('mis-disenyos/editar/<int:pk>/', mis_disenyos_editar, name='mis_disenyos_editar'),
    path('mis-disenyos/borrar/<int:pk>/', mis_disenyos_borrar, name='mis_disenyos_borrar'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

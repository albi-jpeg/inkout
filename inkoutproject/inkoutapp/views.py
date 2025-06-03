from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import *
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .mixins import UserTypeRequiredMixin
from django.db import IntegrityError
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required




# Create your views here.

#Vista de la landing page
class LandpageView(TemplateView):
    template_name = '../templates/landpage.html'

    def get_context_data(self, **kwargs):
        context = super(LandpageView, self).get_context_data(**kwargs)
        context['artistas'] = Artista.objects.all()
        return context
        
#Vista del login        
class LoginView(FormView):
    template_name = '../templates/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('landpage')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class RegistroView(View):
    template_name = 'registro.html'

    def get(self, request):
        form = RegistroUsuarioForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada correctamente. Ahora inicia sesión.')
            return redirect('login')
        return render(request, self.template_name, {'form': form})

#Vista de la ficha de artista    
class ArtistaView(TemplateView):
    template_name = '../templates/artista.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistaView, self).get_context_data(**kwargs)
        context['artista'] = Artista.objects.get(id=kwargs['pk'])
        context['disenyos'] = Disenyo.objects.all()

        return context  

#Vista de la ficha de diseño    
class DisenyoView(TemplateView):
    template_name = '../templates/disenyo.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DisenyoView, self).get_context_data(**kwargs)
        context['disenyo'] = Disenyo.objects.get(id=kwargs['pk'])
        return context  

#Vista de la página de error
class ErrorView(TemplateView):
    template_name = '../templates/error404.html'

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        return context
    
#Vista del perfil de usuario
class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = '../templates/perfil.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_type = user.user_type.lower()

        # Filtrar las citas según el tipo de usuario
        if user_type == 'usuario':
            citas = Cita.objects.filter(usuario=user).order_by('fecha')
        elif user_type == 'artista':
            try:
                artista = user.artista
                citas = Cita.objects.filter(artista=artista).order_by('fecha')
            except Exception:
                citas = []
        elif user_type == 'admin':
            citas = Cita.objects.all().order_by('fecha')
        else:
            citas = []

        context.update({
            'citas': citas,
            'email': user.email,
            'user_type': user.get_user_type_display(),
            'foto_perfil': user.foto_perfil.url if user.foto_perfil else '',
        })
        if user.user_type != 'usuario':
            context['mensajes'] = MensajeContacto.objects.all().order_by('-fecha')

        # Mostrar formulario para editar si llega ?editar=1
        mostrar_formulario = self.request.GET.get('editar') == '1'
        context['mostrar_formulario'] = mostrar_formulario

        # Formulario solo si está editando
        if mostrar_formulario:
            context['form'] = PerfilForm(instance=user)

        return context

    def post(self, request, *args, **kwargs):
        user = request.user

        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        else:
            # En caso de error en el form, mostrarlo de nuevo
            context = self.get_context_data()
            context['form'] = form
            context['mostrar_formulario'] = True
            return self.render_to_response(context)    

#Vista de la ficha de promocion    
class PromoView(LoginRequiredMixin, TemplateView):
    template_name = '../templates/promocion.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PromoView, self).get_context_data(**kwargs)
        context['promocion'] = Promocion.objects.get(id=kwargs['pk'])

        return context
    
#Vista de la página de promociones    
class PromocionesView(TemplateView):
    template_name = '../templates/promociones.html'

    def get_context_data(self,**kwargs):
        context = super(PromocionesView, self).get_context_data(**kwargs)
        context['promociones'] = Promocion.objects.all()
        return context
    
#Vista del formulario para pedir una cita
class PedirCitaView(LoginRequiredMixin, TemplateView):
    template_name = '../templates/cita.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artistas'] = Artista.objects.all() 
        return context

    def post(self, request, *args, **kwargs):
        artista_id = request.POST.get('artista')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        if not all([artista_id, fecha, hora]):
            context = self.get_context_data()
            messages.error(request, 'Por favor, completa todos los campos.')
            return self.render_to_response(context)

        if date.fromisoformat(fecha) < date.today():
            context = self.get_context_data()
            messages.error(request, 'No se puede pedir una cita en una fecha pasada.')
            return self.render_to_response(context)

        artista = Artista.objects.get(id=artista_id)

        try:
            Cita.objects.create(
                artista=artista,
                usuario=request.user,
                fecha=fecha,
                hora=hora,
                estado='pendiente'
            )
            return redirect('perfil')

        except IntegrityError:
            context = self.get_context_data()
            messages.error(request, 'Ya existe una cita con esa fecha. No se puede pedir dos citas para el mismo momento.')
            return self.render_to_response(context)

'''Vista de contacto, no utiliza plantilla propia, 
por lo que añadimos funcionalidades al apartado de contacto de la vista en la que esté'''
class ContactoView(View):
    def post(self, request):
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        if not all([nombre, telefono, asunto, mensaje]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('landpage')  # Asegúrate que 'landpage' sea la URL correcta

        # Guardar mensaje en el modelo
        MensajeContacto.objects.create(
            nombre=nombre,
            telefono=telefono,
            asunto=asunto,
            mensaje=mensaje
        )

        messages.success(request, "¡Mensaje enviado correctamente!")
        return redirect('landpage')
    
# Vistas del administrador para mostrar, añadir, editar y borrar:

#Artista
# Vista para mostrar todos los artistas, es una vista multifunción

def artista_mostrar(request):
    accion = request.GET.get('accion')
    pk = request.GET.get('pk')

    if accion == 'editar':
        artista = get_object_or_404(Artista, pk=pk)
        if request.method == 'POST':
            form = ArtistaForm(request.POST, request.FILES, instance=artista)
            if form.is_valid():
                form.save()
                return redirect('artista_mostrar')
        else:
            form = ArtistaForm(instance=artista)

        return render(request, 'admin.html', {
            'form': form,
            'accion': 'editar',
            'mostrar': 'artistas',
            'artista': artista,
        })

    if accion == 'borrar':
        artista = get_object_or_404(Artista, pk=pk)
        if request.method == 'POST':
            artista.delete()
            return redirect('artista_mostrar')

        return render(request, 'admin.html', {
            'artista': artista,
            'accion': 'borrar',
            'mostrar': 'artistas',
        })

    artistas = Artista.objects.all()
    return render(request, 'admin.html', {
        'artistas': artistas,
        'mostrar': 'artistas',
    })

#Vista para crear un artista
def artista_crear(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artista_mostrar')
    else:
        form = ArtistaForm()

    return render(request, 'admin.html', {
        'form': form,
        'accion': 'crear',
        'mostrar': 'artistas',
    })


#Cita
#Las funcionalidades del modelo artista aplicadas a todos los modelos
def cita_mostrar(request):
    accion = request.GET.get('accion')
    pk = request.GET.get('pk')

    # EDITAR CITA
    if accion == 'editar':
        cita = get_object_or_404(Cita, pk=pk)
        if request.method == 'POST':
            form = CitaForm(request.POST, request.FILES, instance=cita)
            if form.is_valid():
                form.save()
                return redirect('cita_mostrar')
        else:
            form = CitaForm(instance=cita)

        return render(request, 'admin.html', {
            'form': form,
            'accion': 'editar',
            'mostrar': 'citas',
            'cita': cita,
        })

    # BORRAR CITA
    if accion == 'borrar':
        cita = get_object_or_404(Cita, pk=pk)
        if request.method == 'POST':
            cita.delete()
            return redirect('cita_mostrar')

        return render(request, 'admin.html', {
            'cita': cita,
            'accion': 'borrar',
            'mostrar': 'citas',
        })
    
    Cita.objects.filter(fecha__lt=date.today(), estado__in=['pendiente', 'aprobada']).update(estado='vencida')
    # MOSTRAR LISTADO
    citas = Cita.objects.all()
    return render(request, 'admin.html', {
        'citas': citas,
        'mostrar': 'citas'
    })
    
def cita_crear(request):
        if request.method == 'POST':
            form = CitaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('cita_mostrar')
        else:
            form = CitaForm()

        return render(request, 'admin.html', {
            'form': form,
            'accion': 'crear',
            'mostrar': 'citas',
        })

#Diseño
def disenyo_mostrar(request):
    accion = request.GET.get('accion')
    pk = request.GET.get('pk')


    # EDITAR DISEÑO
    if accion == 'editar':
        disenyo = get_object_or_404(Disenyo, pk=pk)
        if request.method == 'POST':
            form = DisenyoForm(request.POST, request.FILES, instance=disenyo)
            if form.is_valid():
                form.save()
                return redirect('disenyo_mostrar')
        else:
            form = DisenyoForm(instance=disenyo)

        return render(request, 'admin.html', {
            'form': form,
            'accion': 'editar',
            'mostrar': 'disenyos',
            'disenyo': disenyo,
        })

    # BORRAR DISEÑO
    if accion == 'borrar':
        disenyo = get_object_or_404(Disenyo, pk=pk)
        if request.method == 'POST':
            disenyo.delete()
            return redirect('disenyo_mostrar')

        return render(request, 'admin.html', {
            'disenyo': disenyo,
            'accion': 'borrar',
            'mostrar': 'disenyos',
        })

    # MOSTRAR LISTADO
    disenyos = Disenyo.objects.all()
    return render(request, 'admin.html', {
        'disenyos': disenyos,
        'mostrar': 'disenyos'
    })
    
def disenyo_crear(request):
    # CREAR DISEÑO
        if request.method == 'POST':
            form = DisenyoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('disenyo_mostrar')
        else:
            form = DisenyoForm()

        return render(request, 'admin.html', {
            'form': form,
            'accion': 'crear',
            'mostrar': 'disenyos',
        })

#Promocion
def promo_mostrar(request):
    accion = request.GET.get('accion')
    pk = request.GET.get('pk')


    # EDITAR PROMOCIÓN
    if accion == 'editar':
        promo = get_object_or_404(Promocion, pk=pk)
        if request.method == 'POST':
            form = PromocionForm(request.POST, request.FILES, instance=promo)
            if form.is_valid():
                form.save()
                return redirect('promo_mostrar')
        else:
            form = PromocionForm(instance=promo)

        return render(request, 'admin.html', {
            'form': form,
            'accion': 'editar',
            'mostrar': 'promos',
            'promo': promo,
        })

    # BORRAR PROMOCIÓN
    if accion == 'borrar':
        promo = get_object_or_404(Promocion, pk=pk)
        if request.method == 'POST':
            promo.delete()
            return redirect('promo_mostrar')

        return render(request, 'admin.html', {
            'promo': promo,
            'accion': 'borrar',
            'mostrar': 'promos',
        })

    # MOSTRAR LISTADO
    promos = Promocion.objects.all()
    return render(request, 'admin.html', {
        'promos': promos,
        'mostrar': 'promos'
    })

def promo_crear(request):
        # CREAR PROMOCIÓN
    if request.method == 'POST':
        form = PromocionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('promo_mostrar')
    else:
        form = PromocionForm()

    return render(request, 'admin.html', {
        'form': form,
        'accion': 'crear',
        'mostrar': 'promos',
    })


#MensajeContacto
#no tiene sentido crear mensajes ni editarlos, por lo tanto la única opción es borrar y mostrar
def mensaje_mostrar(request):
    accion = request.GET.get('accion')
    pk = request.GET.get('pk')


    # BORRAR PROMOCIÓN
    if accion == 'borrar':
        mensaje = get_object_or_404(MensajeContacto, pk=pk)
        if request.method == 'POST':
            mensaje.delete()
            return redirect('mensaje_mostrar')

        return render(request, 'admin.html', {
            'mensaje': mensaje,
            'accion': 'borrar',
            'mostrar': 'mensajes',
        })

    # MOSTRAR LISTADO
    mensajes = MensajeContacto.objects.all()
    return render(request, 'admin.html', {
        'mensajes': mensajes,
        'mostrar': 'mensajes'
    })


@login_required
def mis_disenyos(request):
    if request.user.user_type != 'artista':
        return HttpResponseForbidden("No tienes permiso para acceder aquí.")

    disenyos = Disenyo.objects.filter(artista__usuario=request.user)
    return render(request, 'artista_disenyos.html', {
        'disenyos': disenyos,
        'accion': None,
    })


@login_required
def mis_disenyos_crear(request):
    if request.user.user_type != 'artista':
        return HttpResponseForbidden("No tienes permiso para acceder aquí.")
    
    artista = request.user.artista
    if request.method == 'POST':
        form = DisenyoForm(request.POST, request.FILES)
        if form.is_valid():
            disenyo = form.save(commit=False)
            disenyo.artista = artista
            disenyo.save()
            return redirect('mis_disenyos')
    else:
        form = DisenyoForm()

    return render(request, 'artista_disenyos.html', {
        'form': form,
        'accion': 'crear',
    })


@login_required
def mis_disenyos_editar(request, pk):
    disenyo = get_object_or_404(Disenyo, pk=pk, artista__usuario=request.user)

    if request.method == 'POST':
        form = DisenyoForm(request.POST, request.FILES, instance=disenyo)
        if form.is_valid():
            form.save()
            return redirect('mis_disenyos')
    else:
        form = DisenyoForm(instance=disenyo)

    return render(request, 'artista_disenyos.html', {
        'form': form,
        'accion': 'editar',
    })


@login_required
def mis_disenyos_borrar(request, pk):
    disenyo = get_object_or_404(Disenyo, pk=pk, artista__usuario=request.user)

    if request.method == 'POST':
        disenyo.delete()
        return redirect('mis_disenyos')

    return render(request, 'artista_disenyos.html', {
        'objeto': disenyo,
        'accion': 'borrar',
    })

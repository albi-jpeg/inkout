from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from inkoutapp.models import *
from login import *
from usuarios.models import *
from inkoutapp.mixins import *
from inkoutapp.forms import ArtistaForm, CitaForm, DisenyoForm, PromocionForm

class AdminPanelView(UserTypeRequiredMixin, TemplateView):
    template_name = '../templates/admin.html'
    required_user_type = 'admin'

    def get_context_data(self, **kwargs):
        context = super(AdminPanelView, self).get_context_data(**kwargs)

        # Incluir todos los formularios en el contexto SIEMPRE
        context['form_artista'] = ArtistaForm()
        context['form_cita'] = CitaForm()
        context['form_diseno'] = DisenyoForm()
        context['form_promocion'] = PromocionForm()

        # Mostrar listas solo si se solicita por GET
        mostrar = self.request.GET.get('mostrar')
        if mostrar == 'artistas':
            context['artistas'] = Artista.objects.all()
        elif mostrar == 'citas':
            context['citas'] = Cita.objects.all()
        elif mostrar == 'disenos':
            context['disenos'] = Disenyo.objects.all()
        elif mostrar == 'promociones':
            context['promociones'] = Promocion.objects.all()

        return context

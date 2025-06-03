from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from .models import MyUser
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from inkoutapp.forms import *
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

# Vistas del administrador para mostrar, añadir, editar y borrar:
#Usuario

def usuario_mostrar(request):
    accion = request.GET.get('accion')
    pk = request.GET.get('pk')

    # EDITAR USUARIO
    if accion == 'editar':
        usuario = get_object_or_404(MyUser, pk=pk)
        if request.method == 'POST':
            form = UsuarioForm(request.POST, request.FILES, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('usuario_mostrar')
        else:
            form = UsuarioForm(instance=usuario)

        return render(request, 'admin.html', {
            'form': form,
            'accion': 'editar',
            'mostrar': 'usuarios',
            'usuario': usuario,
        })


    # BORRAR USUARIO
    if accion == 'borrar':
        usuario = get_object_or_404(MyUser, pk=pk)
        if request.method == 'POST':
            usuario.delete()
            return redirect('usuario_mostrar')

        return render(request, 'admin.html', {
            'usuario': usuario,
            'accion': 'borrar',
            'mostrar': 'usuarios',
        })

    # MOSTRAR LISTADO DE USUARIOS
    usuarios = MyUser.objects.all()
    return render(request, 'admin.html', {
        'usuarios': usuarios,
        'mostrar': 'usuarios'
    })

def usuario_crear(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('usuario_mostrar')
    else:
        form = UsuarioForm()

    return render(request, 'admin.html', {
        'form': form,
        'accion': 'crear',
        'mostrar': 'usuarios',
    })

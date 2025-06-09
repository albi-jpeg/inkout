from django.shortcuts import render
from django import forms
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Create your views here.

#Vista Login
class LoginFormView(LoginView):
    template_name = '../templates/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión'
        return context
    
    def get_success_url(self):
        return reverse_lazy('landpage') 
    
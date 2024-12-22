from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django.contrib.auth.forms import AuthenticationForm
import siscentroconciliacionjj.settings as setting
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class IniciarSesionFormView(LoginView):
    form_class = AuthenticationForm
    template_name = 'iniciarsesion/iniciarsesion.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

class LoginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = 'iniciarsesion/iniciarsesion.html'
    success_url = reverse_lazy('ccjj:jj_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

class CerrarSesionFormView(RedirectView):
    
    pattern_name = 'ccjj:jj_iniciarsesion'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
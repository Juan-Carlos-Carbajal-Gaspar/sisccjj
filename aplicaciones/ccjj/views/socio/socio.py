from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# IMPORTANDON CLASES CRUD DE DJANGO
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

import siscentroconciliacionjj.settings as setting
from django.contrib.auth import authenticate, login, logout

# IMPORTANDO MODELO PERSONA Y CLIENTE
from aplicaciones.ccjj.models import Persona, Socio

# IMPORTANDO FORMULARIO SOCIO
from aplicaciones.ccjj.forms.socio.socio import SocioForm

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Create your views here.
# Listar Socios
class ListaSocio(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Socio
    template_name = "socio/listasocio.html"
    permission_required = 'view_socio'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listasocio':
                data = []
                for i in Socio.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Socios'
        context['titleform']='SOCIOS'
        # context['formcli'] = ClienteForm()
        context['list_url']=reverse_lazy('ccjj:jj_listasocio')
        context['crear_url']=reverse_lazy('ccjj:jj_crearsocio')
        return context

# Metodo para Crear Socio
class CrearSocio(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Socio
    form_class = SocioForm
    template_name = 'socio/crearsocio.html'
    success_url = reverse_lazy('ccjj:jj_listasocio')
    permission_required = 'add_socio'
    # permission_required = 'add_category'
    # url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'crearsocio':
                per=Persona()
                per.nom_per=request.POST['nom_per']
                per.apepat_per=request.POST['apepat_per']
                per.apemat_per=request.POST['apemat_per']
                per.numdoc_per=request.POST['numdoc_per']
                per.eda_per=request.POST['eda_per']
                per.sex_per=request.POST['sex_per']
                per.dir_per=request.POST['dir_per']
                per.numcel_per=request.POST['numcel_per']
                per.ema_per=request.POST['ema_per']
                per.save()

                soc=Socio()
                soc.cod_soc="Cod" + per.numdoc_per
                soc.id_per_id=per.id               
                soc.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Nuevo Socio'
        context['titleform']='Nuevo Socio'
        context['action'] = 'crearsocio'
        context['tipoaction'] = 'add'
        context['read_url'] = self.success_url
               
        return context

# Metodo para Editar Socio
class EditarSocio(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Persona
    form_class = SocioForm
    template_name = 'socio/editarsocio.html'
    success_url = reverse_lazy('ccjj:jj_listasocio')
    permission_required = 'change_socio'

    url_redirect = success_url

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'editarsocio':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Socio'
        context['titleform']='Editar Socio'
        context['action'] = 'editarsocio'
        context['tipoaction'] = 'edit'
        context['read_url'] = self.success_url

        return context

class EliminarSocio(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Persona
    template_name = 'socio/eliminarsocio.html'
    success_url = reverse_lazy('ccjj:jj_listasocio')
    # permission_required = 'delete_category'
    permission_required = 'delete_socio'

    # url_redirect = success_url

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            soc= Socio.objects.get(id_per=self.kwargs.get('pk'))
            soc.delete()
            per=Persona.objects.get(pk=self.kwargs.get('pk'))
            per.delete()
            
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Socio'
        context['titleform']='Eliminar Socio'
        context['read_url'] = self.success_url

        return context
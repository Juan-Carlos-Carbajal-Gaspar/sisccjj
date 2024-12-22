from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# IMPORTANDON CLASES CRUD DE DJANGO
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

import siscentroconciliacionjj.settings as setting
from django.contrib.auth import authenticate, login, logout

# IMPORTANDO MODELO PERSONA Y CLIENTE
from aplicaciones.ccjj.models import Persona, Cliente
# IMPORTANDO FORM CLIENTE
from aplicaciones.ccjj.forms.cliente.cliente import ClienteForm

# Create your views here.
# Listar Clientes
class ListaCliente(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Cliente
    template_name = "cliente/listacliente.html"
    permission_required = 'view_cliente'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listacliente':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Clientes (Partes en conflicto)'
        context['titleform']='CLIENTES - PARTES EN CONFLICTO'
        # context['formcli'] = ClienteForm()
        context['list_url']=reverse_lazy('ccjj:jj_listacliente')
        context['crear_url']=reverse_lazy('ccjj:jj_crearcliente')
    
        return context

class CrearCliente(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crearcliente.html'
    success_url = reverse_lazy('ccjj:jj_listacliente')
    permission_required = 'add_cliente'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'crearcliente':
                      
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

                cli=Cliente()
                cli.id_per_id=per.id
                cli.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Nuevo Cliente'
        context['titleform']='Nuevo Cliente'
        context['action'] = 'crearcliente'
        context['tipoaction'] = 'add'
        context['read_url'] = self.success_url
               
        return context
    
class EditarCliente(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Persona
    form_class = ClienteForm
    template_name = 'cliente/editarcliente.html'
    success_url = reverse_lazy('ccjj:jj_listacliente')
    permission_required = 'change_cliente'
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
            if action == 'editarcliente':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['titleform']='Editar Cliente'
        context['action'] = 'editarcliente'
        context['tipoaction'] = 'edit'
        context['read_url'] = self.success_url

        return context
    
class EliminarCliente(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Persona
    template_name = 'cliente/eliminarcliente.html'
    success_url = reverse_lazy('ccjj:jj_listacliente')
    # permission_required = 'delete_category'
    permission_required = 'delete_cliente'
    # url_redirect = success_url

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            cli = Cliente.objects.get(id_per=self.kwargs.get('pk'))
            cli.delete()
            per=Persona.objects.get(pk=self.kwargs.get('pk'))
            per.delete()
            
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cliente'
        context['titleform']='Eliminar Cliente'
        context['read_url'] = self.success_url

        return context
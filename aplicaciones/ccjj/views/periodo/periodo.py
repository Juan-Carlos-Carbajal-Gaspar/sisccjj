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
from aplicaciones.ccjj.models import Periodo
# IMPORTANDO FORM CLIENTE
from aplicaciones.ccjj.forms.periodo.periodo import PeriodoForm

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Create your views here.
# Listar Clientes
class ListaPeriodo(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Periodo
    template_name = "periodo/listaperiodo.html"
    permission_required = 'view_periodo'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'readperiodo':
                data = []
                for i in Periodo.objects.all().order_by('-id'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Periodo'
        context['titleform']='PERIODO'
        # context['formcli'] = ClienteForm()
        context['list_url']=reverse_lazy('ccjj:jj_listaperiodo')
        context['crear_url']=reverse_lazy('ccjj:jj_crearperiodo')
    
        return context

class CrearPeriodo(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = "periodo/crearperiodo.html"
    success_url = reverse_lazy('ccjj:jj_listaperiodo')
    permission_required = 'add_periodo'
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
            if action == 'crearperiodo':
                      
                conf=Periodo()
                conf.per_pe=request.POST['per_pe']
                conf.num_exp=request.POST['num_exp']
                conf.num_act=request.POST['num_act']
                conf.num_inf=request.POST['num_inf']
                conf.est_pe=request.POST['est_pe']
                conf.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Nuevo Periodo'
        context['titleform']='Nuevo Periodo'
        context['action'] = 'crearperiodo'
        context['tipoaction'] = 'add'
        context['read_url'] = self.success_url
               
        return context
    
class EditarPeriodo(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = "periodo/editarperiodo.html"
    success_url = reverse_lazy('ccjj:jj_listaperiodo')
    permission_required = 'change_periodo'
    # permission_required = 'change_category'
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
            if action == 'editarperiodo':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Perido'
        context['titleform']='Editar Periodo'
        context['action'] = 'editarperiodo'
        context['tipoaction'] = 'edit'
        context['read_url'] = self.success_url

        return context
    
# class EliminarCliente(DeleteView):
#     model = Persona
#     template_name = 'cliente/eliminarcliente.html'
#     success_url = reverse_lazy('ccjj:jj_listacliente')
#     # permission_required = 'delete_category'
#     # url_redirect = success_url

#     @method_decorator(csrf_exempt)
#     @method_decorator(login_required)

#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             cli = Cliente.objects.get(id_per=self.kwargs.get('pk'))
#             cli.delete()
#             per=Persona.objects.get(pk=self.kwargs.get('pk'))
#             per.delete()
            
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Eliminar Cliente'
#         context['titleform']='Eliminar Cliente'
#         context['read_url'] = self.success_url

#         return context
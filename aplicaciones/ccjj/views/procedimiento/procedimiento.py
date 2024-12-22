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

# IMPORTANDO MODELO MATERIA
from aplicaciones.ccjj.models import Procedimiento
# IMPORTANDO FORM CLIENTE
from aplicaciones.ccjj.forms.procedimiento.procedimiento import ProcedimientoForm

# Create your views here.
# Listar Clientes
class ListaProcedimiento(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Procedimiento
    template_name = "procedimiento/listaprocedimiento.html"
    permission_required = 'view_procedimiento'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listaprocedimiento':
                data = []
                for i in Procedimiento.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Procedimientos Conciliables'
        context['titleform']='PROCEDIMIENTOS CONCILIABLES'
        context['list_url']=reverse_lazy('ccjj:jj_listaprocedimiento')
        context['crear_url']=reverse_lazy('ccjj:jj_crearprocedimiento')
    
        return context

class CrearProcedimiento(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Procedimiento
    form_class = ProcedimientoForm
    template_name = 'procedimiento/crearprocedimiento.html'
    success_url = reverse_lazy('ccjj:jj_listaprocedimiento')
    permission_required = 'add_procedimiento'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'crearprocedimiento':
                      
                mat=Procedimiento()
                mat.des_pro=request.POST['des_pro']
                mat.id_mat_id=request.POST['id_mat']
                mat.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Nuevo Procedimiento'
        context['titleform']='Nuevo Procedimiento'
        context['action'] = 'crearprocedimiento'
        context['tipoaction'] = 'add'
        context['read_url'] = self.success_url
               
        return context
    
class EditarProcedimiento(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Procedimiento
    form_class = ProcedimientoForm
    template_name = 'procedimiento/editarprocedimiento.html'
    success_url = reverse_lazy('ccjj:jj_listaprocedimiento')
    permission_required = 'change_procedimiento'
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
            if action == 'editarprocedimiento':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Procedimiento'
        context['titleform']='Editar Procedimiento'
        context['action'] = 'editarprocedimiento'
        context['tipoaction'] = 'edit'
        context['read_url'] = self.success_url

        return context
    

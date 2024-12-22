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
from aplicaciones.ccjj.models import Especificacion
# IMPORTANDO FORM CLIENTE
from aplicaciones.ccjj.forms.especificacion.especificacion import EspecificacionForm

# Create your views here.
# Listar Clientes
class ListaEspecificacion(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Especificacion
    template_name = "especificacion/listaespecificacion.html"
    permission_required = 'view_especificacion'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listaespecificacion':
                data = []
                for i in Especificacion.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Especificaciones Conciliables'
        context['titleform']='ESPECIFICACIONES CONCILIABLES'
        context['list_url']=reverse_lazy('ccjj:jj_listaespecificacion')
        context['crear_url']=reverse_lazy('ccjj:jj_crearespecificacion')
    
        return context

class CrearEspecificacion(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Especificacion
    form_class = EspecificacionForm
    template_name = 'especificacion/crearespecificacion.html'
    success_url = reverse_lazy('ccjj:jj_listaespecificacion')
    permission_required = 'add_especificacion'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'crearespecificacion':
                      
                esp=Especificacion()
                esp.des_esp=request.POST['des_esp']
                esp.cos_esp=request.POST['cos_esp']
                esp.id_pro_id=request.POST['id_pro']
                esp.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Nueva Especificacion'
        context['titleform']='Nueva Especificacion'
        context['action'] = 'crearespecificacion'
        context['tipoaction'] = 'add'
        context['read_url'] = self.success_url
               
        return context
    
class EditarEspecificacion(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Especificacion
    form_class = EspecificacionForm
    template_name = 'especificacion/editarespecificacion.html'
    success_url = reverse_lazy('ccjj:jj_listaespecificacion')
    permission_required = 'change_especificacion'
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
            if action == 'editarespecificacion':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Especificacion'
        context['titleform']='Editar Especificacion'
        context['action'] = 'editarespecificacion'
        context['tipoaction'] = 'edit'
        context['read_url'] = self.success_url

        return context
    

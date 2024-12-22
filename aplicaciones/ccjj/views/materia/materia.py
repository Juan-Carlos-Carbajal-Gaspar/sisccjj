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
from aplicaciones.ccjj.models import Materia
# IMPORTANDO FORM CLIENTE
from aplicaciones.ccjj.forms.materia.materia import MateriaForm

# Create your views here.
# Listar Clientes
class ListaMateria(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Materia
    template_name = "materia/listamateria.html"
    permission_required = 'view_materia'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listamateria':
                data = []
                for i in Materia.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Materias Conciliables'
        context['titleform']='MATERIAS CONCILIABLES'
        context['list_url']=reverse_lazy('ccjj:jj_listamateria')
        context['crear_url']=reverse_lazy('ccjj:jj_crearmateria')
    
        return context

class CrearMateria(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'materia/crearmateria.html'
    success_url = reverse_lazy('ccjj:jj_listamateria')
    permission_required = 'add_materia'
    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'crearmateria':
                      
                mat=Materia()
                mat.des_mat=request.POST['des_mat']
                mat.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Nueva Materia'
        context['titleform']='Nueva Materia'
        context['action'] = 'crearmateria'
        context['tipoaction'] = 'add'
        context['read_url'] = self.success_url
               
        return context
    
class EditarMateria(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'materia/editarmateria.html'
    success_url = reverse_lazy('ccjj:jj_listamateria')
    permission_required = 'change_materia'
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
            if action == 'editarmateria':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Materia'
        context['titleform']='Editar Materia'
        context['action'] = 'editarmateria'
        context['tipoaction'] = 'edit'
        context['read_url'] = self.success_url

        return context
    

import os
from inspect import isfunction
from pydoc import Doc
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# IMPORTANDON CLASES CRUD DE DJANGO
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

import siscentroconciliacionjj.settings as setting
from django.contrib.auth import authenticate, login, logout
# IMPORTANDO CLASE EXPEDIENTEDATOS
from aplicaciones.ccjj.views.conciliacion.expediente.expedientedatos import ExpedienteDatos
# IMPORTANDO MODELO EXPEDIENTE
from aplicaciones.ccjj.models import CajaConciliacion, Documento, Especificacion, Expediente, Solicitud, Invitacion
from aplicaciones.user.models import User
# from django.contrib.auth.models import User
# IMPORTANDO FORM DOCUMENTOS
from aplicaciones.ccjj.forms.conciliacion.documentos.documentos import DocumentoForm

from siscentroconciliacionjj.settings import STATIC_URL, STATIC_URL, MEDIA_URL, MEDIA_ROOT

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin


# Create your views here.

# Listar Expedientes
class ListaDocumentos(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
   
    template_name = "conciliacion/documentos/listadocumentos.html"
    permission_required = 'change_documento'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listadocumentos':
                data = []
                for i in Documento.objects.filter(id_exp = self.kwargs.get('pk')):
                    data.append(i.toJSON())
            elif action == 'subirdocumento':
                arch_exp= Documento.objects.get(pk=request.POST['id'])
                arch_exp.arcesc_doc = request.FILES['archivo']
                arch_exp.save()
            elif action == 'listaotrosdocumentos':
                data = []
                for i in Invitacion.objects.select_related("id_inv").filter(id_inv__id_exp = self.kwargs.get('pk')):
                    data.append(i.toJSON())
            elif action == 'subirotrosdocumento':
                invi= Invitacion.objects.get(pk=request.POST['id'])
                invi.esc_invi = request.FILES['otroarchivo']
                invi.save()
                                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Documentos'
        context['titleform']='DOCUMENTOS DE CONCILIACION'
        context['idexp'] = self.kwargs.get('pk')
        context['action'] = 'subirdocumento'
        context['list_url']=reverse_lazy('ccjj:jj_listadocumentos')
        context['formdocumento'] = DocumentoForm()
        # context['crear_url']=reverse_lazy('ccjj:jj_crearcliente')
    
        return context

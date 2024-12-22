from ipaddress import v4_int_to_packed
import json
import os
import io
from datetime import datetime
from inspect import isfunction
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# IMPORTANDON CLASES CRUD DE DJANGO
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.db import transaction

import siscentroconciliacionjj.settings as setting
from django.contrib.auth import authenticate, login, logout
# IMPORTANDO CLASE SOLICITUDDATOS
from aplicaciones.ccjj.views.conciliacion.solicitud.solicituddatos import SolicitudDatos
# IMPORTANDO CLASE EXPEDIENTEDATOS
from aplicaciones.ccjj.views.conciliacion.expediente.expedientedatos import ExpedienteDatos
# IMPORTANDO MODELO EXPEDIENTE
from aplicaciones.ccjj.models import Periodo, Documento, Especificacion, Expediente, Materia, Persona, Procedimiento, Solicitante, Solicitud, Cliente
from django.contrib.auth.models import User
# IMPORTANDO FORM MATERIACONCILIACION
from aplicaciones.ccjj.forms.conciliacion.materiaconciliacion.materiaconciliacion import MateriaConciliacionForm

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Create your views here.
class SeleccionarMateriaConciliacion(LoginRequiredMixin, ValidatePermissionRequiredMixin, FormView):
    model = Materia
    form_class = MateriaConciliacionForm
    template_name = 'conciliacion/materiaconciliacion/materiaconciliacion.html'
    # success_url = reverse_lazy('ccjj:jj_dashboard')
    permission_required = 'change_materia'
    # url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Para Seleccionar Materias Conciliables
            action = request.POST['action']
            if action == 'search_procedimientos_id':
                data = [{'id': '', 'text': '---'}]
                for i in Procedimiento.objects.filter(id_mat=request.POST['id']):
                    data.append({'id': i.id, 'text': i.des_pro})
            elif action == 'search_especificaciones_id':
                data = [{'id': '', 'text': '---'}]
                for i in Especificacion.objects.filter(id_pro=request.POST['id']):
                    data.append({'id': i.id, 'text': i.des_esp + ' | Costo S/. ' + str(i.cos_esp) })
            elif action == 'crearmateriaconciliacion':
                # Agregamos materia conciliable al expediente
                desmat=''

                exp = Expediente.objects.get(pk=self.kwargs.get('pk'))
                exp.id_esp_id=request.POST['especificaciones']

                for i in Materia.objects.filter(pk=request.POST['materias']):
                    desmat=i.des_mat
                
                exp.proini_exp=desmat + '-PROCEDIMIENTO INICIADO'
                exp.esttra_exp=desmat + '-EN TRAMITE'
                exp.estpro_exp = 'mat'
                exp.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Materia de Conciliacion'
        context['titleform'] = 'Materia de Conciliacion'
        context['action'] = 'crearmateriaconciliacion'
        context['formmatcon'] = MateriaConciliacionForm()
        context['idexp'] = self.kwargs.get('pk')
        
        # context['read_url'] = self.success_url

        return context
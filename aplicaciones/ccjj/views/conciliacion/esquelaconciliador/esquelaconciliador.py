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
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.db import transaction

import siscentroconciliacionjj.settings as setting
from django.contrib.auth import authenticate, login, logout
# IMPORTANDO CLASE SOLICITUDDATOS
from aplicaciones.ccjj.views.conciliacion.solicitud.solicituddatos import SolicitudDatos
# IMPORTANDO CLASE EXPEDIENTEDATOS
from aplicaciones.ccjj.views.conciliacion.expediente.expedientedatos import ExpedienteDatos
# IMPORTANDO MODELO EXPEDIENTE
from aplicaciones.ccjj.models import Conciliador, Periodo, Documento, Especificacion, Expediente, Persona, Solicitante, Solicitud, Cliente
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# IMPORTANDO FORM EXPEDIENTE
from aplicaciones.ccjj.forms.conciliacion.solicitud.solicitud import SolicitudForm
# IMPORTANDO CLASE ESQUELA CONCILIADOR DATOS
from aplicaciones.ccjj.views.conciliacion.esquelaconciliador.esquelaconciliadordatos import EsquelaConciliadorDatos


# Para utilizar algunas de las funciones de la librería de pydocx
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

# Palantillas word
from docxtpl import DocxTemplate
import jinja2
# import pandas as pd

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Create your views here.
class CrearEsquelaConciliador(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    model = Conciliador
    
    template_name = 'conciliacion/esquelaconciliador/crearesquelaconciliador.html'
    permission_required = 'add_conciliador'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # Para buscar solicitante e invitado
            if action == 'searchconciliadores':
                data = [{'id': '', 'text': 'Seleccionar'}]
                for i in Group.objects.get(name='Conciliador').user_set.all():
                    data.append({'id': i.id, 'text': i.first_name + ' ' + i.last_name  })
            elif action == 'crearesquelaconciliador':

                idexp = self.kwargs.get('pk')
                esqcondatos = EsquelaConciliadorDatos()

                # Agregamos Esquela Conciliador
                con = Conciliador()
                con.fec_doc=esqcondatos.fecha()
                con.hor_doc=esqcondatos.hora()
                con.id_exp_id=idexp
                con.save()
                
                # Actualizamos Expediente
                exp=Expediente.objects.get(pk=idexp)
                exp.id_user_id=request.POST['conciliador']
                if exp.tipcon_exp == 'ma':
                    exp.estpro_exp = 'inv'
                else:
                    exp.estpro_exp='esq'
                exp.save()

                # Agregamos Documento Solicitud
                docesqcon = Documento()
                docesqcon.tip_doc = 'ESQUELA CONCILIADOR DEL EXPEDIENTE N° ' + str(esqcondatos.numExpediente(idexp) + '-' + str(esqcondatos.yearExpediente(idexp)))
                docesqcon.arcesc_doc = ''
                docesqcon.t_doc = 'esquela'
                docesqcon.id_exp_id = idexp
                docesqcon.save()
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Esquela Conciliador'
        context['titleform'] = 'Esquela Conciliador'
        context['action'] = 'crearesquelaconciliador'
        # context['read_url'] = self.success_url

        context['idexp'] = self.kwargs.get('pk')
        return context

# Generar Solicitud Word
def generarEsquelaConciliador(self, pk):
    idexp=pk
    # Clase EsquelaConciliadorDoc
    esqcondatos = EsquelaConciliadorDatos()

    fecha=datetime.now()

    docesqconciliador = DocxTemplate('plantillasdoc/plantillaesquelaconciliador.docx')
    context={
        'numexp': esqcondatos.numExpediente(idexp),
        'year': esqcondatos.yearExpediente(idexp),
        'terminoconciliador': esqcondatos.terminoConciliador(idexp),
        'conciliador': esqcondatos.datosConciliador(idexp),
        'registro': esqcondatos.datosRegistroNoFamilia(idexp),
        'registrofamilia': esqcondatos.datosRegistroFamilia(idexp),
        'termdesignacion': esqcondatos.datosTermDesignacion(idexp),
        'solicitantes': esqcondatos.datosSolicitantes(idexp),
        'invitados': esqcondatos.datosInvitados(idexp),
        'procedimiento': esqcondatos.datosProcedimiento(idexp),
        'fechaesqcon': 'Huancayo, ' + fecha.strftime("%d de %B del año " + str(esqcondatos.yearExpediente(idexp)))
    }
    docesqconciliador.render(context)

    document_data = io.BytesIO()
    docesqconciliador.save(document_data)
    document_data.seek(0)
    response = HttpResponse(document_data.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    response["Content-Disposition"] = 'attachment; filename = "Esquela Conciliador Expediente N° '+ str(esqcondatos.numExpediente(idexp)) + '-' + str(esqcondatos.yearExpediente(idexp)) + '.docx"'
    response["Content-Encoding"] = "UTF-8"
    return response
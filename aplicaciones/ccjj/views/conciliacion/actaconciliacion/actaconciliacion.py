from distutils.command import sdist
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
from aplicaciones.ccjj.models import Acta, Conciliador, Periodo, Documento, Especificacion, Expediente, Informe, Parcial, Persona, Solicitante, Solicitud, Cliente, IngresoConciliacion, Agenda
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# IMPORTANDO FORM ACTA DE CONCILIACION
from aplicaciones.ccjj.forms.conciliacion.actaconciliacion.actaconciliacion import ActaConciliacionForm
# IMPORTANDO CLASE Acta
from aplicaciones.ccjj.views.conciliacion.actaconciliacion.actaconciliaciondatos import ActaDoc


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
class CrearActaConciliacion(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):

    model = Informe
    
    template_name = 'conciliacion/actaconciliacion/actaconciliacion.html'
    permission_required = 'add_informe'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def fecha(self):
        fechaactual=datetime.now()
        for i in Periodo.objects.filter(est_pe='a'):
            fechaexp=i.per_pe
        return fechaexp + '-' + fechaactual.strftime("%m-%d")
    
    def hora(self):
        horaactual=datetime.now()
        return horaactual.strftime('%H:%M:%S')
    
    # Year Acta
    def yearActa(self):
        for i in Periodo.objects.filter(est_pe='a'):
            return i.per_pe

    # Funcion para saber el numero de Acta
    def numeroActa(self):
        numacta=0
        for i in Periodo.objects.filter(est_pe='a'):
            numacta=int(i.num_act)
        return numacta
    
    # Numero de Parcial
    def numeroParcial(self):
        numpar = 0
        for i in Periodo.objects.filter(est_pe='a'):
            numpar = int(i.num_inf)            
        return numpar
    
    # Funcion para saber el tipo de conciliacion del expediente
    def tipoConciliacion(self,**kwargs):
        tipcon=''
        for i in Expediente.objects.filter(id=self.kwargs.get('pk')):
            tipcon= i.tipcon_exp
        return tipcon
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # Para buscar solicitante e invitado
            if action == 'crearactaconciliacion':
                # Clase Acta
                actadoc=ActaDoc()

                inf = Informe()
                inf.tip_inf = request.POST['tip_inf']
                inf.fec_inf = self.fecha()
                inf.hor_inf = self.hora()
                inf.id_exp_id = self.kwargs.get('pk')
                inf.save()

                if request.POST['tip_inf'] == 'ci':

                    par = Parcial()
                    par.num_par = self.numeroParcial()
                    par.id_inf_id = inf.id
                    par.save()

                    # Para actualizar Expediente
                    exp = Expediente.objects.get(id=self.kwargs.get('pk'))
                    exp.esttra_exp = ''
                    if self.tipoConciliacion()=='ma':
                        exp.inv_exp='NINGUNA'
                    exp.estact_exp='CI'
                    exp.estpro_exp = 'act'
                    exp.save()

                    # Para actualizar Configuracion
                    conf=Periodo.objects.get(est_pe='a')
                    conf.num_inf=int(self.numeroParcial())+1
                    conf.save()

                    # Agregamos Documento Parcial
                    docinf = Documento()
                    docinf.tip_doc = 'INFORME DEL EXPEDIENTE N° ' + str(actadoc.numExpediente(self.kwargs.get('pk'))) + '-' + self.yearActa()
                    docinf.arcesc_doc = ''
                    docinf.t_doc = 'informeacta'
                    docinf.id_exp_id = self.kwargs.get('pk')
                    docinf.save()
                else:
                    act = Acta()
                    act.num_act = request.POST['numacta']
                    act.id_inf_id = inf.id
                    act.save()

                    # Para actualizar Configuracion
                    conf=Periodo.objects.get(est_pe='a')
                    conf.num_act=int(request.POST['numacta'])+1
                    conf.save()

                    # Para actualizar Expediente
                    exp = Expediente.objects.get(id=self.kwargs.get('pk'))
                    exp.esttra_exp = ''
                    if self.tipoConciliacion()=='ma':
                        exp.inv_exp='NINGUNA'
                    exp.estact_exp='CA'
                    exp.estpro_exp = 'act'
                    exp.save()

                    # Agregamos Documento Acta
                    docinf = Documento()
                    docinf.tip_doc = 'ACTA DEL EXPEDIENTE N° ' + str(actadoc.numExpediente(self.kwargs.get('pk'))) + '-' + self.yearActa()
                    docinf.arcesc_doc = ''
                    docinf.t_doc = 'informeacta'
                    docinf.id_exp_id = self.kwargs.get('pk')
                    docinf.save()

                # Actualizamos dato FINALIZADO/NO FINALIZADO en Expediente
                for caj in IngresoConciliacion.objects.filter(idcaj_con__id_exp = self.kwargs.get('pk')):
                    pactado = caj.pacpag_con
                    pagoadelanto = caj.pagpacade_con

                datexp = Expediente.objects.get(id = self.kwargs.get('pk'))
                if pactado == pagoadelanto:
                    datexp.confin_exp = 'FINALIZADO'
                else:
                    datexp.confin_exp = 'NO FINALIZADO'
                datexp.save()

                # Eliminamos agenda
                if(self.tipoConciliacion() == 'ci'):
                    age = Agenda.objects.get(id_exp = self.kwargs.get('pk'))
                    age.delete()                
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Acta de Conciliacion'
        context['titleform'] = 'Acta de Conciliacion'
        context['action'] = 'crearactaconciliacion'
        context['idexp'] = self.kwargs.get('pk')
        context['numacta'] = self.numeroActa()
        context['numparcial'] = self.numeroParcial()
        context['tipinv'] = self.tipoConciliacion()
        

        fecha=datetime.now()
        context['formactaconciliacion'] = ActaConciliacionForm(fecha.strftime(self.yearActa() + "-%m-%d %H:%M:%S"))
        return context

# Generar Informe Acta o Parcial Word
def generarActa(self, pk):
    idexp=pk
    # Clase Acta
    actadoc=ActaDoc()

    fecha=datetime.now()

    docacta = DocxTemplate('plantillasdoc/plantillaActa.docx')
    
    context={
        'numexp': actadoc.numExpediente(idexp),
        'year': actadoc.yearActa(idexp),
        'numacta': actadoc.numActaParcial(idexp),
        'tipacta': actadoc.tipoInforme(idexp),
        'hora': actadoc.hora(),
        'fechadia': actadoc.fechaActa(idexp),
        'conciliador': actadoc.conciliadorActa(idexp),
        'dni': actadoc.conciliadorDNI(idexp),
        'termconciliador': actadoc.terminoConciliador(idexp),
        'registro': actadoc.registro(idexp),
        'termsolicitantes': actadoc.terminoSolicitantes(idexp),
        'solicitantes': actadoc.datosSolicitantes(idexp),
        'terminvitados': actadoc.terminoInvitados(idexp),
        'invitados': actadoc.datosInvitados(idexp),
        'hechos': actadoc.datosHechos(idexp),
        'descripcion': actadoc.datosDescripcion(idexp),
        'firmas': actadoc.datosFirmas(idexp),
    }
    
    docacta.render(context)

    document_data = io.BytesIO()
    docacta.save(document_data)
    document_data.seek(0)
    response = HttpResponse(document_data.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    response["Content-Disposition"] = 'attachment; filename = "Acta de Conciliacion N° '+ str(actadoc.numExpediente(idexp)) + '-' + str(actadoc.yearActa(idexp)) + '.docx"'
    response["Content-Encoding"] = "UTF-8"
    return response
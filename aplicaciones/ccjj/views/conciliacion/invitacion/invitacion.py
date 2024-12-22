from genericpath import exists
import json
import os
import io

from datetime import datetime
from django.shortcuts import render

# Importando modelos de Base de Datos
from aplicaciones.ccjj.models import Agenda, Expediente, Invitacion, Invitado, Documento
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db import transaction
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Importando la clase TemplateView
from django.views.generic.base import TemplateView

# IMPORTANDO CLASE INVITACIONDOC
from aplicaciones.ccjj.views.conciliacion.invitacion.invitaciondatos import InvitacionDoc

# Palantillas word
from docxtpl import DocxTemplate
import jinja2

import locale
locale.setlocale(locale.LC_ALL, 'es_Pe')

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Creando nuestra vista para la Solicitud

class CrearInvitaciónConciliacionView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    
    template_name = "conciliacion/invitacion/invitacion.html"
    permission_required = 'add_invitacion'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            fecha=datetime.now()
            idexp = self.kwargs.get('pk')
            action = request.POST['action']

            if action == 'searchdatainvitados':
                data = []
                datainvitado={}

                for i in Invitado.objects.select_related('id_per').filter(id_exp=idexp):
                    datainvitado['id'] = i.id
                    datainvitado['idper'] = i.id_per.id
                    datainvitado['dni'] = i.id_per.numdoc_per
                    datainvitado['invitado'] = i.id_per.nom_per + " " + i.id_per.apepat_per + " " + i.id_per.apemat_per
                    
                    if Invitacion.objects.filter(id_inv = i.id).exists():

                        for inv in Invitacion.objects.filter(id_inv = i.id):
                            datainvitado['fechainv'] = inv.fec_invi
                            datainvitado['horainv'] = inv.hor_invi
                            datainvitado['ninvitacion'] = inv.tip_invi                   
                    else:
                        datainvitado['fechainv'] = ''
                        datainvitado['horainv'] = ''
                        datainvitado['ninvitacion'] = '0'

                    # Para validar si existe acta
                    for e in Expediente.objects.filter(id = idexp):
                        estadopro = e.estpro_exp
                    datainvitado['estadopro'] = estadopro

                    data.append(datainvitado)
                    datainvitado={}
            
            elif action == 'buscardatosinvitacion':
                
                data = []

                for i in Invitacion.objects.select_related('id_inv').filter(id_inv__id_exp=idexp).order_by('-id'):
                    data.append(i.tip_invi)                 
                    data.append(i.fec_invi)
                    data.append(i.hor_invi)
                print(data)
                    
            elif action == 'addprimera':
                # Inicializamos variables de uso
                fechahora = datetime.strptime(str(request.POST['txtfechahora']), "%Y-%m-%dT%H:%M")
                print(fechahora)
                    
                fecha = str(fechahora.year) + '-' + str(fechahora.month)+ '-' + str(fechahora.day)
                hora = str(fechahora.hour) + ':' + str(fechahora.minute)+ ':' + str(fechahora.second)
                
                ######################################################

                # Guardamos Invitacion
                priinv = Invitacion()
                priinv.tip_invi = 'p'
                priinv.fec_invi = fecha
                priinv.hor_invi = hora
                priinv.esc_invi = ''
                priinv.id_inv_id = request.POST['id']
                priinv.save()

                # Guardamos Agenda
                if Agenda.objects.filter(id_exp = idexp, tipinvi_age='p').count() == 0:
                    # Agregamos Agenda
                    age=Agenda()
                    age.tit_age = 'Primera I. - Exp. ' + str(idexp)
                    age.des_age = 'Primera I. - Exp. ' + str(idexp)
                    age.tipinvi_age = 'p'
                    age.fecaud_age = fechahora
                    age.borcolor_age = ''
                    age.foncolor_age = ''
                    age.id_exp_id = idexp
                    age.save()

                # Actualizamos Datos de Expediente
                exp = Expediente.objects.get(pk=idexp)
                exp.inv_exp = 'PRIMERA'
                exp.estpro_exp = 'caj'
                exp.save()

                #######################################################
            elif action == 'addsegunda':
                # Inicializamos variables de uso
                fechahora = datetime.strptime(str(request.POST['txtfechahoras']), "%Y-%m-%dT%H:%M")
                print(fechahora)
                    
                fecha = str(fechahora.year) + '-' + str(fechahora.month)+ '-' + str(fechahora.day)
                hora = str(fechahora.hour) + ':' + str(fechahora.minute)+ ':' + str(fechahora.second)
                
                ######################################################

                # Guardamos Invitacion
                priinv = Invitacion()
                priinv.tip_invi = 's'
                priinv.fec_invi = fecha
                priinv.hor_invi = hora
                priinv.esc_invi = ''
                priinv.id_inv_id = request.POST['ids']
                priinv.save()

                # Guardamos Agenda
                if Agenda.objects.filter(id_exp = idexp, tipinvi_age='s').count() == 0:
                    # Agregamos Agenda
                    # Actualizamos Datos de Agenda
                    age = Agenda.objects.get(id_exp=idexp)
                    age.tit_age = 'Segunda I. - Exp. ' + str(idexp)
                    age.des_age = 'Segunda I. - Exp. ' + str(idexp)
                    age.tipinvi_age = 's'
                    age.fecaud_age = fechahora
                    age.save()

                # Actualizamos Datos de Expediente
                exp = Expediente.objects.get(pk=idexp)
                exp.inv_exp = 'SEGUNDA'
                exp.estpro_exp = 'caj'
                exp.save()
                #######################################################
            else:
                data['error'] = 'Ha ocurrido un error'                
           
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Invitación Conciliacion'
        # context['forminicio']=ConfiguracionForm()
        context['titleform']='Invitación Conciliacion'
        context['idexp'] = self.kwargs.get('pk')
        context['action'] = 'crearinvitacion'
        # context['fechaactual'] = datetime.now()
        
        return context
    
def generarPrimeraInvitacion(self, pk, id, fecha):
    datafecha=datetime.now()

    idexp = pk
    idper = id

    # Clase InvitacionDoc
    invidoc=InvitacionDoc()

    docinvitacion = DocxTemplate('plantillasdoc/plantillaInvitacion.docx')
    context={
        'numexp': invidoc.numExpediente(idexp),
        'year': invidoc.yearExpediente(idexp),
        'tipinvitacion': 'PRIMERA',
        'solicitantes': invidoc.datosSolicitantes(idexp),
        'direccionsolicitantes': invidoc.datosDireccionSolicitantes(idexp),
        'invitado': invidoc.datosInvitados(idper),
        'direccioninvitado': invidoc.datosDireccionInvitados(idper),
        'fechaaudiencia': fecha,
        'pretensionsol': invidoc.datosPretensionSol(idexp),
        'textoinvitacion': 'presente',
        'fechadoc': 'Huancayo, ' + datafecha.strftime("%d de %B del año " + str(invidoc.yearExpediente(idexp))),
    }
    docinvitacion.render(context)

    document_data = io.BytesIO()
    docinvitacion.save(document_data)
    document_data.seek(0)
    response = HttpResponse(document_data.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    response["Content-Disposition"] = 'attachment; filename = "Primera Invitación de ' + invidoc.datosInvitados(idper) + ' - ' + str(invidoc.numExpediente(idexp)) + '-' + str(invidoc.yearExpediente(idexp)) +'.docx"'
    response["Content-Encoding"] = "UTF-8"
    return response

def generarSegundaInvitacion(self, pk, id, fecha):
    datafecha=datetime.now()

    idexp = pk
    idper = id

    # Clase InvitacionDoc
    invidoc=InvitacionDoc()

    docinvitacion = DocxTemplate('plantillasdoc/plantillaInvitacion.docx')
    context={
        'numexp': invidoc.numExpediente(idexp),
        'year': invidoc.yearExpediente(idexp),
        'tipinvitacion': 'SEGUNDA',
        'solicitantes': invidoc.datosSolicitantes(idexp),
        'direccionsolicitantes': invidoc.datosDireccionSolicitantes(idexp),
        'invitado': invidoc.datosInvitados(idper),
        'direccioninvitado': invidoc.datosDireccionInvitados(idper),
        'fechaaudiencia': fecha,
        'pretensionsol': invidoc.datosPretensionSol(idexp),
        'textoinvitacion': 'primera',
        'fechadoc': 'Huancayo, ' + datafecha.strftime("%d de %B del año " + str(invidoc.yearExpediente(idexp))),
    }
    docinvitacion.render(context)

    document_data = io.BytesIO()
    docinvitacion.save(document_data)
    document_data.seek(0)
    response = HttpResponse(document_data.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    response["Content-Disposition"] = 'attachment; filename = "Segunda Invitación de ' + invidoc.datosInvitados(idper) + ' - ' + str(invidoc.numExpediente(idexp)) + '-' + str(invidoc.yearExpediente(idexp)) +'.docx"'
    response["Content-Encoding"] = "UTF-8"
    return response


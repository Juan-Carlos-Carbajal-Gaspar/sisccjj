import json
import os
import io

from datetime import datetime

# Importando modelos de Base de Datos
from aplicaciones.ccjj.models import Expediente, Cliente, Periodo, Invitado, Solicitante, Solicitud, Cliente, Persona, Socio, CajaConciliacion, IngresoConciliacion, IngresoConciliacionDetalle, IngresoCopias, EgresoDetalle
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

# Importando Formulario IngresConciliacionForm
from aplicaciones.ccjj.forms.conciliacion.ingresoconciliacion.ingresoconciliacion import IngresoConciliacionForm
# IMPORTANDO FORMULARIO SOCIO
from aplicaciones.ccjj.forms.socio.socio import SocioForm
# IMPORTANDO CLASE ESQUELA CONCILIADOR DATOS
from aplicaciones.ccjj.views.conciliacion.ingresoconciliacion.recibodatos import ReciboDatos

# Para utilizar algunas de las funciones de la librería de pydocx
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

# Palantillas word
from docxtpl import DocxTemplate
import jinja2
# import pandas as pd


import locale
locale.setlocale(locale.LC_ALL, 'es_Pe')

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Creando nuestra vista para la Solicitud

class CrearIngresoConciliacionView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    
    template_name = "conciliacion/ingresoconciliacion/ingresoconciliacion.html"
    permission_required = 'add_ingresoconciliacion'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Funcion para cuanto fue pactado el expediente
    def pagoPactadoExpediente(self,**kwargs):
        pagoexptotal=0
        dataexppago=Expediente.objects.select_related('id_esp').filter(id=self.kwargs.get('pk'))
        for i in dataexppago:
            pagoexptotal= i.id_esp.cos_esp
        return pagoexptotal

    # Funcion para saber el tipo de conciliacion del expediente
    def tipoConciliacion(self,**kwargs):
        tipcon=''
        datatipocon=Expediente.objects.filter(id=self.kwargs.get('pk'))
        for i in datatipocon:
            tipcon= i.tipcon_exp
        return tipcon

    def fecha(self):
        fechaactual=datetime.now()
        for i in Periodo.objects.filter(est_pe='a'):
            fechaexp=i.per_pe
        return fechaexp + '-' + fechaactual.strftime("%m-%d")
    
    def hora(self):
        fechaactual=datetime.now()

        return fechaactual.strftime("%H:%M:%S")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            fecha=datetime.now()
            action = request.POST['action']
            
            # Para crear un buscar clientes
            if action == 'searchcliente':
                data = [{'id': '', 'text': 'Seleccionar'}]
                for i in Solicitante.objects.filter(id_exp=self.kwargs.get('pk')):
                    data.append({'id': i.id_per.id, 'text': i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per  })
                for i in Invitado.objects.filter(id_exp=self.kwargs.get('pk')):
                    data.append({'id': i.id_per.id, 'text': i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per })
                
            # Para crear un nuevo Socio
            elif action == 'create_socio':
                with transaction.atomic():
                    
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

                    soc=Socio()
                    soc.cod_soc="Cod" + per.numdoc_per
                    soc.id_per_id=per.id               
                    soc.save()
            
            elif action == 'crearingresoconciliacion':
                # Agregamos datos de caja conciliacion
                cajexp = CajaConciliacion()
                cajexp.ing_con = float(request.POST['adelanto'])
                cajexp.ingcop_con = 0
                cajexp.toting_con = float(request.POST['adelanto'])
                cajexp.egre_con = 0
                cajexp.id_exp_id = self.kwargs.get('pk')
                cajexp.id_soc_id = request.POST['socios']
                cajexp.save()

                # Agregarmos Ingreso Conciliacion
                ingcon = IngresoConciliacion()
                ingcon.pacpag_con = float(self.pagoPactadoExpediente()) - float(request.POST['descuento'])
                ingcon.desc_con = float(request.POST['descuento'])
                ingcon.pagpacade_con = float(request.POST['adelanto'])

                if(ingcon.pagpacade_con == ingcon.pacpag_con):
                    ingcon.estado_con = 'CANCELADO'
                else:
                    ingcon.estado_con = 'NO CANCELADO'
                
                ingcon.idcaj_con_id = cajexp.id
                ingcon.save()

                # Agregamos Ingreso Conciliacion Detalle
                ingcondet = IngresoConciliacionDetalle()
                ingcondet.monadedet_con = float(request.POST['adelanto'])
                ingcondet.fecingdet_con = self.fecha()
                ingcondet.horingdet_con = self.hora()
                ingcondet.id_cli_id = request.POST['cliente']
                ingcondet.idpag_con_id = ingcon.id
                ingcondet.save()

                # Actualizamos Expediente
                exp=Expediente.objects.get(pk=self.kwargs.get('pk'))
                exp.estpro_exp='caj'
                exp.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingreso Conciliacion'
        # context['forminicio']=ConfiguracionForm()
        context['titleform']='Ingreso Conciliacion'
        context['idexp'] = self.kwargs.get('pk')
        context['tipcon'] = self.tipoConciliacion()
        context['action'] = 'crearingresoconciliacion'
        context['formpagoexp'] = IngresoConciliacionForm(self.pagoPactadoExpediente())
        context['formsocio'] = SocioForm()
        return context
    
class CajaConciliacionView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    
    template_name = "conciliacion/ingresoconciliacion/cajaconciliacion.html"
    permission_required = 'add_cajaconciliacion'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Funcion para cuanto fue pactado el expediente
    def pagoPactadoExpediente(self,**kwargs):
        pagoexptotal=0
        dataexppago=Expediente.objects.select_related('id_esp').filter(id=self.kwargs.get('pk'))
        for i in dataexppago:
            pagoexptotal= i.id_esp.cos_esp
        return pagoexptotal
    
    # Funcion para cuanto fue el descuento
    def dataIngresoDetalleConciliacion(self,**kwargs):
        dataingreso={}
    
        for i in IngresoConciliacion.objects.select_related('idcaj_con').filter(idcaj_con__id_exp=self.kwargs.get('pk')):
            dataingreso['descuento'] = i.desc_con
            dataingreso['pactado'] = i.pacpag_con
            dataingreso['montotaladel'] = i.pagpacade_con
            dataingreso['montodeuda'] = i.pacpag_con - i.pagpacade_con
            dataingreso['estado'] = i.estado_con
                        
        return dataingreso

    # Funcion para saber el tipo de conciliacion del expediente
    def tipoConciliacion(self,**kwargs):
        tipcon=''
        datatipocon=Expediente.objects.filter(id=self.kwargs.get('pk'))
        for i in datatipocon:
            tipcon= i.tipcon_exp
        return tipcon

    def fecha(self):
        fechaactual=datetime.now()
        for i in Periodo.objects.filter(est_pe='a'):
            fechaexp=i.per_pe
        return fechaexp + '-' + fechaactual.strftime("%m-%d")
    
    def hora(self):
        fechaactual=datetime.now()

        return fechaactual.strftime("%H:%M:%S")
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            fecha=datetime.now()
            action = request.POST['action']
                        
            # Para crear un buscar clientes
            if action == 'listacajaconciliacion':
                data = []
                for i in CajaConciliacion.objects.filter(id_exp=self.kwargs.get('pk')):
                    data.append(i.toJSON())
            elif action == 'searchcliente':
                data = [{'id': '', 'text': 'Seleccionar'}]
                for i in Solicitante.objects.filter(id_exp=self.kwargs.get('pk')):
                    data.append({'id': i.id_per.id, 'text': i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per })
                for i in Invitado.objects.filter(id_exp=self.kwargs.get('pk')):
                    data.append({'id': i.id_per.id, 'text': i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per })

            elif action == 'listaingresodetalleconciliacion':
                dataing = []
                dataingreso={}

                for i in IngresoConciliacionDetalle.objects.select_related('idpag_con').filter(idpag_con__idcaj_con__id_exp=self.kwargs.get('pk')):
                    dataingreso['fechapago'] = i.fecingdet_con
                    dataingreso['horapago'] = i.horingdet_con
                    dataingreso['montoadelantado'] = i.monadedet_con
                    dataingreso['iddet']=i.id

                    for per in Persona.objects.filter(id=i.id_cli_id):
                        dataingreso['cliente'] = per.nom_per + ' ' + per.apepat_per + ' ' + per.apemat_per       

                    dataing.append(dataingreso)
                    dataingreso={}

                data = dataing 
            elif action == 'ingresaringresoconciliaciondetalle':
                # Agregamos IngresoConciliacionDetalle
                ingdetcon = IngresoConciliacionDetalle()
                ingdetcon.monadedet_con = request.POST['adelanto']
                ingdetcon.fecingdet_con = self.fecha()
                ingdetcon.horingdet_con = self.hora()
                ingdetcon.id_cli_id = request.POST['cliente']

                for i in IngresoConciliacionDetalle.objects.select_related('idpag_con').filter(idpag_con__idcaj_con__id_exp=self.kwargs.get('pk')):
                    ingdetcon.idpag_con_id = i.idpag_con.id
                ingdetcon.save()

                # Actualizamos datos de IngresoConciliacion
                ingcon = IngresoConciliacion.objects.get(idcaj_con__id_exp=self.kwargs.get('pk'))
                ingcon.pagpacade_con = ingcon.pagpacade_con + float(request.POST['adelanto'])
                ingcon.save()

                # Actualizamos datos de CajaConciliacion
                cajcon = CajaConciliacion.objects.get(id_exp=self.kwargs.get('pk'))
                cajcon.ing_con = cajcon.ing_con + float(request.POST['adelanto'])
                cajcon.toting_con = cajcon.ing_con + cajcon.ingcop_con
                cajcon.save()

                # Consultamos Datos Ingreso Conciliacion
                for ingcon in IngresoConciliacion.objects.filter(idcaj_con__id_exp = self.kwargs.get('pk')):
                    montopactado = ingcon.pacpag_con
                    montoadelanto = ingcon.pagpacade_con
                
                # Actualizamos Datos Ingreso Conciliacion / Estado
                inco = IngresoConciliacion.objects.get(idcaj_con__id_exp=self.kwargs.get('pk'))
                if(montopactado == montoadelanto):
                    inco.estado_con = 'CANCELADO'
                else:
                    inco.estado_con = 'NO CANCELADO'
                inco.save()

                # Actulizamos datos Expediente
                if(montoadelanto == montopactado):
                    exp=Expediente.objects.get(id=self.kwargs.get('pk'))
                    if (exp.estpro_exp == 'act'):
                        exp.confin_exp = 'FINALIZADO'
                        exp.save()

            elif action == 'ingresocopiaacta':
                # Agregamos Ingreso Copias Acta
                ingrecopiasact = IngresoCopias()
                ingrecopiasact.monpag_cop = float(request.POST['montocopias'])
                ingrecopiasact.cancop_cop = float(request.POST['cantidadcopias'])
                ingrecopiasact.fec_cop = self.fecha()
                ingrecopiasact.hor_cop = self.hora()
                ingrecopiasact.id_cli_id = request.POST['clienteacta']

                for datacaja in CajaConciliacion.objects.filter(id_exp = self.kwargs.get('pk')):
                    ingrecopiasact.idcaj_con_id = datacaja.id
                ingrecopiasact.save()

                # Actualizamos datos de CajaConciliacion
                cajcon = CajaConciliacion.objects.get(id_exp=self.kwargs.get('pk'))
                cajcon.ingcop_con = float(cajcon.ingcop_con) + float(request.POST['montocopias'])
                cajcon.toting_con = float(cajcon.ing_con) + float(cajcon.ingcop_con)
                cajcon.save()
            elif action == 'listaingresocopiasacta':
                dataingc = []
                dataingresoc={}

                for ic in IngresoCopias.objects.filter(idcaj_con__id_exp=self.kwargs.get('pk')):
                    dataingresoc['fechapago'] = ic.fec_cop
                    dataingresoc['horapago'] = ic.hor_cop
                    dataingresoc['montocopias'] = ic.monpag_cop
                    dataingresoc['cantidad'] = ic.cancop_cop
                    dataingresoc['idingcop'] = ic.id
            
                    for per in Persona.objects.filter(id=ic.id_cli_id):
                        dataingresoc['cliente'] = per.nom_per + ' ' + per.apepat_per + ' ' + per.apemat_per       

                    dataingc.append(dataingresoc)
                    dataingresoc={}
                                        
                data = dataingc 
            elif action == 'listaegresosconciliacion':
                dataegre = []
                dataingredat={}

                for edc in EgresoDetalle.objects.filter(idcaj_con__id_exp=self.kwargs.get('pk')):
                    dataingredat['fechaegreso'] = edc.fecegredet_con
                    dataingredat['horaegreso'] = edc.horegredet_con
                    dataingredat['tipinvi'] = edc.tipinv_con
                    dataingredat['montoegreso'] = edc.monegre_det
                    
                    dataegre.append(dataingredat)
                    dataingredat={}
                data = dataegre
            elif action == 'addegresos':
                # Agregamos Egresos Conciliacion
                egrecon = EgresoDetalle()
                egrecon.monegre_det = request.POST['montoegresos']
                egrecon.fecegredet_con = self.fecha()
                egrecon.horegredet_con = self.hora()
                egrecon.tipinv_con = request.POST['tipoinv']

                for datacaja in CajaConciliacion.objects.filter(id_exp = self.kwargs.get('pk')):
                    egrecon.idcaj_con_id = datacaja.id
                egrecon.save()

                # Actualizamos datos de CajaConciliacion
                cajcon = CajaConciliacion.objects.get(id_exp=self.kwargs.get('pk'))
                cajcon.egre_con = cajcon.egre_con + float(request.POST['montoegresos'])
                cajcon.save()
            
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Caja Conciliación'
        # context['forminicio']=ConfiguracionForm()
        context['titleform']='Caja Conciliación'
        context['idexp'] = self.kwargs.get('pk')
        context['tipcon'] = self.tipoConciliacion()
        context['action'] = 'crearingresoconciliacion'
        context['formpagoexp'] = IngresoConciliacionForm(self.pagoPactadoExpediente())
        context['dataingreso'] = self.dataIngresoDetalleConciliacion()
        context['formsocio'] = SocioForm()

        return context

# Generar Recibo ingreso conciliacion
def generarRecibo(self, pk):
    iddet = pk

    # Clase ReciboDatos
    recdatos = ReciboDatos()

    fecha=datetime.now()

    docrecibo = DocxTemplate('plantillasdoc/plantillaRecibo.docx')
    context={
        'cliente': recdatos.datosCliente(iddet),
        'dni': recdatos.datosDNI(iddet),
        'monto': recdatos.montoAbono(iddet),
        'fecha': fecha.strftime("%d de %B del año " + str(recdatos.yearExpediente()))
    }
    docrecibo.render(context)

    document_data = io.BytesIO()
    docrecibo.save(document_data)
    document_data.seek(0)
    response = HttpResponse(document_data.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    response["Content-Disposition"] = 'attachment; filename = "Recibo de Pago - '+ str(recdatos.datosCliente(iddet)) + '.docx"'
    response["Content-Encoding"] = "UTF-8"
    return response

# Generar Recibo ingreso copias
def generarReciboCopias(self, pk):
    idcop = pk

    # Clase ReciboDatos
    recdatos = ReciboDatos()

    fecha=datetime.now()

    docrecibo = DocxTemplate('plantillasdoc/plantillaReciboCopias.docx')
    context={
        'cliente': recdatos.datosClienteCopias(idcop),
        'dni': recdatos.datosDNICopias(idcop),
        'monto': recdatos.montoAbonoCopias(idcop),
        'fecha': fecha.strftime("%d de %B del año " + str(recdatos.yearExpediente()))
    }
    docrecibo.render(context)

    document_data = io.BytesIO()
    docrecibo.save(document_data)
    document_data.seek(0)
    response = HttpResponse(document_data.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    response["Content-Disposition"] = 'attachment; filename = "Recibo de Pago - '+ str(recdatos.datosClienteCopias(idcop)) + '.docx"'
    response["Content-Encoding"] = "UTF-8"
    return response
    

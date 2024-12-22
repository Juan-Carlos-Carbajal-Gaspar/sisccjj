from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from aplicaciones.ccjj.models import Cliente, Periodo, Procedimiento, Materia
from aplicaciones.ccjj.views.reportes.rtrimestral.ReporteTrimestralAll import ReporteTrimestralAll

from datetime import datetime, timedelta

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Create your views here.

class ReporteTrimestralView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'reportes/rtrimestral/rtrimestral.html'
    permission_required = 'view_acta'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'searchyear':
                data = [{'id': '0', 'text': 'Seleccionar'}]
                for i in Periodo.objects.all():
                    data.append({'id': i.per_pe, 'text': i.per_pe})
                print(data)
            elif action == 'searchall':
                fechdesde = request.POST['fechdesde']
                fechhasta = request.POST['fechhasta']
                materia = request.POST['materia']
                rt=ReporteTrimestralAll()
                # Prueba 1
                data= []
                datart=[]

                for p in Procedimiento.objects.filter(id_mat=materia):
                    datart.append(p.des_pro)
                    datart.append(rt.datosProcedimientosIniciados(p.id, fechdesde, fechhasta)) # Enviar id
                    datart.append(rt.datosEnTramite(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoAcuerdoTotal(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoAcuerdoParcial(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoFaltaAcuerdo(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoInasistenciaSolicitante(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoInasistenciaInvitado(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoInasistenciaAmbasPartes(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoDesicionMotivaConciliador(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosConcluidoInforme(p.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidos(p.id, fechdesde, fechhasta))
                        
                    data.append(datart)
                    datart=[]

            elif action == 'searchallmateria':
                fechdesde = request.POST['fechdesde']
                fechhasta = request.POST['fechhasta']
                materia = request.POST['materia']
                rt=ReporteTrimestralAll()
                # Prueba 1
                data= []
                datart=[]

                for m in Materia.objects.filter(id=materia):
                    datart.append('TOTAL')
                    datart.append(rt.datosTotalProcedimientosIniciados(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalEstadoTramite(m.id, fechdesde, fechhasta))                 
                    datart.append(rt.datosTotalConcluidoAcuerdoTotal(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidoAcuerdoParcial(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidoFaltaAcuerdo(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidoInasistenciaSolicitante(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidoInasistenciaInvitado(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidoInasistenciaAmbasPartes(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidoDesicionMotivaConciliador(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidoInforme(m.id, fechdesde, fechhasta))
                    datart.append(rt.datosTotalConcluidosTotal(m.id, fechdesde, fechhasta))
                    data.append(datart)
                    datart=[]
            elif action == 'searchallgeneral':
                fechdesde = request.POST['fechdesde']
                fechhasta = request.POST['fechhasta']

                rt=ReporteTrimestralAll()
                # Prueba 1
                data= []
                datart=[]

                datart.append('TOTAL GENERAL')
                datart.append(rt.datosTotalGeneralProcedimientosIniciados(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralEstadoTramite(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoAcuerdoTotal(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoAcuerdoParcial(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoFaltaAcuerdo(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoInasistenciaSolicitante(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoInasistenciaInvitado(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoInasistenciaAmbasPartes(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoDesicionMotivaConciliador(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidoInforme(fechdesde, fechhasta))
                datart.append(rt.datosTotalGeneralConcluidosTotal(fechdesde, fechhasta))
                
                data.append(datart)
                datart=[]
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Trimestral'
        context['titleform']='REPORTE TRIMESTRAL'
               
        return context

class ReporteTrimestralInvoicePdf(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    def fechaDesdeValidar(self, year, desde):
        if desde == 'ENERO':
            return year + '-01-01'
        elif desde == 'ABRIL':
            return year + '-04-01'
        elif desde == 'JULIO':
            return year + '-07-01'
        elif desde == 'OCTUBRE':
            return year + '-10-01'
            
    def fechaHastaValidar(self, year, hasta):
        if hasta == 'MARZO':
            return year + '-03-31'
        elif hasta == 'JUNIO':
            return year + '-06-30'
        elif hasta == 'SEPTIEMBRE':
            return year + '-09-30'
        elif hasta == 'DICIEMBRE':
            return year + '-12-31'

    def get(self, request, *args, **kwargs):
        desde = self.kwargs['fechadesde']
        hasta = self.kwargs['fechahasta']
        yearpdf = self.kwargs['year']
        fechdesde = self.fechaDesdeValidar(str(yearpdf), desde)
        fechhasta = self.fechaHastaValidar(str(yearpdf), hasta)

        rt=ReporteTrimestralAll()
        # Materia Civil
        datacivil= []
        datartcivil={}
        for p in Procedimiento.objects.filter(id_mat=2):
            datartcivil['proc']=p.des_pro
            datartcivil['procini']=rt.datosProcedimientosIniciados(p.id, fechdesde, fechhasta) # Enviar id
            datartcivil['entram']=rt.datosEnTramite(p.id, fechdesde, fechhasta)
            datartcivil['cat']=rt.datosConcluidoAcuerdoTotal(p.id, fechdesde, fechhasta)
            datartcivil['cap']=rt.datosConcluidoAcuerdoParcial(p.id, fechdesde, fechhasta)
            datartcivil['cfa']=rt.datosConcluidoFaltaAcuerdo(p.id, fechdesde, fechhasta)
            datartcivil['ciups']=rt.datosConcluidoInasistenciaSolicitante(p.id, fechdesde, fechhasta)
            datartcivil['ciupi']=rt.datosConcluidoInasistenciaInvitado(p.id, fechdesde, fechhasta)
            datartcivil['ciap']=rt.datosConcluidoInasistenciaAmbasPartes(p.id, fechdesde, fechhasta)
            datartcivil['cdmc']=rt.datosConcluidoDesicionMotivaConciliador(p.id, fechdesde, fechhasta)
            datartcivil['cci']=rt.datosConcluidoInforme(p.id, fechdesde, fechhasta)
            datartcivil['cti']=rt.datosTotalConcluidos(p.id, fechdesde, fechhasta)
                        
            datacivil.append(datartcivil)
            datartcivil={}
        # Materia Civil Total
        dataciviltotal= []
        datartciviltotal={}

        for m in Materia.objects.filter(id=2):
            datartciviltotal['tprocini']=rt.datosTotalProcedimientosIniciados(m.id, fechdesde, fechhasta)
            datartciviltotal['tentram']=rt.datosTotalEstadoTramite(m.id, fechdesde, fechhasta)
            datartciviltotal['tcat']=rt.datosTotalConcluidoAcuerdoTotal(m.id, fechdesde, fechhasta)
            datartciviltotal['tcap']=rt.datosTotalConcluidoAcuerdoParcial(m.id, fechdesde, fechhasta)
            datartciviltotal['tcfa']=rt.datosTotalConcluidoFaltaAcuerdo(m.id, fechdesde, fechhasta)
            datartciviltotal['tciups']=rt.datosTotalConcluidoInasistenciaSolicitante(m.id, fechdesde, fechhasta)
            datartciviltotal['tciupi']=rt.datosTotalConcluidoInasistenciaInvitado(m.id, fechdesde, fechhasta)
            datartciviltotal['tciap']=rt.datosTotalConcluidoInasistenciaAmbasPartes(m.id, fechdesde, fechhasta)
            datartciviltotal['tcdmc']=rt.datosTotalConcluidoDesicionMotivaConciliador(m.id, fechdesde, fechhasta)
            datartciviltotal['tcci']=rt.datosTotalConcluidoInforme(m.id, fechdesde, fechhasta)
            datartciviltotal['tcti']=rt.datosTotalConcluidosTotal(m.id, fechdesde, fechhasta)
            dataciviltotal.append(datartciviltotal)
            datartciviltotal={}
        
        # Materia Familia
        datafamilia= []
        datartfamilia={}
        for p in Procedimiento.objects.filter(id_mat=1):
            datartfamilia['proc']=p.des_pro
            datartfamilia['procini']=rt.datosProcedimientosIniciados(p.id, fechdesde, fechhasta) # Enviar id
            datartfamilia['entram']=rt.datosEnTramite(p.id, fechdesde, fechhasta)
            datartfamilia['cat']=rt.datosConcluidoAcuerdoTotal(p.id, fechdesde, fechhasta)
            datartfamilia['cap']=rt.datosConcluidoAcuerdoParcial(p.id, fechdesde, fechhasta)
            datartfamilia['cfa']=rt.datosConcluidoFaltaAcuerdo(p.id, fechdesde, fechhasta)
            datartfamilia['ciups']=rt.datosConcluidoInasistenciaSolicitante(p.id, fechdesde, fechhasta)
            datartfamilia['ciupi']=rt.datosConcluidoInasistenciaInvitado(p.id, fechdesde, fechhasta)
            datartfamilia['ciap']=rt.datosConcluidoInasistenciaAmbasPartes(p.id, fechdesde, fechhasta)
            datartfamilia['cdmc']=rt.datosConcluidoDesicionMotivaConciliador(p.id, fechdesde, fechhasta)
            datartfamilia['cci']=rt.datosConcluidoInforme(p.id, fechdesde, fechhasta)
            datartfamilia['cti']=rt.datosTotalConcluidos(p.id, fechdesde, fechhasta)
                        
            datafamilia.append(datartfamilia)
            datartfamilia={}
        
        # Materia Familia Total
        datafamiliatotal= []
        datartfamiliatotal={}

        for m in Materia.objects.filter(id=1):
            datartfamiliatotal['tprocini']=rt.datosTotalProcedimientosIniciados(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tentram']=rt.datosTotalEstadoTramite(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tcat']=rt.datosTotalConcluidoAcuerdoTotal(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tcap']=rt.datosTotalConcluidoAcuerdoParcial(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tcfa']=rt.datosTotalConcluidoFaltaAcuerdo(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tciups']=rt.datosTotalConcluidoInasistenciaSolicitante(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tciupi']=rt.datosTotalConcluidoInasistenciaInvitado(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tciap']=rt.datosTotalConcluidoInasistenciaAmbasPartes(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tcdmc']=rt.datosTotalConcluidoDesicionMotivaConciliador(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tcci']=rt.datosTotalConcluidoInforme(m.id, fechdesde, fechhasta)
            datartfamiliatotal['tcti']=rt.datosTotalConcluidosTotal(m.id, fechdesde, fechhasta)
            datafamiliatotal.append(datartfamiliatotal)
            datartfamiliatotal={}
        
        # Materia Contraciones Con El Estado
        dataestado= []
        datartestado={}
        for p in Procedimiento.objects.filter(id_mat=3):
            datartestado['proc']=p.des_pro
            datartestado['procini']=rt.datosProcedimientosIniciados(p.id, fechdesde, fechhasta) # Enviar id
            datartestado['entram']=rt.datosEnTramite(p.id, fechdesde, fechhasta)
            datartestado['cat']=rt.datosConcluidoAcuerdoTotal(p.id, fechdesde, fechhasta)
            datartestado['cap']=rt.datosConcluidoAcuerdoParcial(p.id, fechdesde, fechhasta)
            datartestado['cfa']=rt.datosConcluidoFaltaAcuerdo(p.id, fechdesde, fechhasta)
            datartestado['ciups']=rt.datosConcluidoInasistenciaSolicitante(p.id, fechdesde, fechhasta)
            datartestado['ciupi']=rt.datosConcluidoInasistenciaInvitado(p.id, fechdesde, fechhasta)
            datartestado['ciap']=rt.datosConcluidoInasistenciaAmbasPartes(p.id, fechdesde, fechhasta)
            datartestado['cdmc']=rt.datosConcluidoDesicionMotivaConciliador(p.id, fechdesde, fechhasta)
            datartestado['cci']=rt.datosConcluidoInforme(p.id, fechdesde, fechhasta)
            datartestado['cti']=rt.datosTotalConcluidos(p.id, fechdesde, fechhasta)
                        
            dataestado.append(datartestado)
            datartestado={}

        # Materia Contrataciones Con EL Estado Total
        dataestadototal= []
        datartestadototal={}

        for m in Materia.objects.filter(id=3):
            datartestadototal['tprocini']=rt.datosTotalProcedimientosIniciados(m.id, fechdesde, fechhasta)
            datartestadototal['tentram']=rt.datosTotalEstadoTramite(m.id, fechdesde, fechhasta)
            datartestadototal['tcat']=rt.datosTotalConcluidoAcuerdoTotal(m.id, fechdesde, fechhasta)
            datartestadototal['tcap']=rt.datosTotalConcluidoAcuerdoParcial(m.id, fechdesde, fechhasta)
            datartestadototal['tcfa']=rt.datosTotalConcluidoFaltaAcuerdo(m.id, fechdesde, fechhasta)
            datartestadototal['tciups']=rt.datosTotalConcluidoInasistenciaSolicitante(m.id, fechdesde, fechhasta)
            datartestadototal['tciupi']=rt.datosTotalConcluidoInasistenciaInvitado(m.id, fechdesde, fechhasta)
            datartestadototal['tciap']=rt.datosTotalConcluidoInasistenciaAmbasPartes(m.id, fechdesde, fechhasta)
            datartestadototal['tcdmc']=rt.datosTotalConcluidoDesicionMotivaConciliador(m.id, fechdesde, fechhasta)
            datartestadototal['tcci']=rt.datosTotalConcluidoInforme(m.id, fechdesde, fechhasta)
            datartestadototal['tcti']=rt.datosTotalConcluidosTotal(m.id, fechdesde, fechhasta)
            dataestadototal.append(datartestadototal)
            datartestadototal={}

        # Total General de Todas las Materias
        dataestadototalgeneral= []
        datartestadototalgeneral={}

        for m in Materia.objects.filter(id=3):
            datartestadototalgeneral['tgprocini']=rt.datosTotalGeneralProcedimientosIniciados(fechdesde, fechhasta)
            datartestadototalgeneral['tgentram']=rt.datosTotalGeneralEstadoTramite(fechdesde, fechhasta)
            datartestadototalgeneral['tgcat']=rt.datosTotalGeneralConcluidoAcuerdoTotal(fechdesde, fechhasta)
            datartestadototalgeneral['tgcap']=rt.datosTotalGeneralConcluidoAcuerdoParcial(fechdesde, fechhasta)
            datartestadototalgeneral['tgcfa']=rt.datosTotalGeneralConcluidoFaltaAcuerdo(fechdesde, fechhasta)
            datartestadototalgeneral['tgciups']=rt.datosTotalGeneralConcluidoInasistenciaSolicitante(fechdesde, fechhasta)
            datartestadototalgeneral['tgciupi']=rt.datosTotalGeneralConcluidoInasistenciaInvitado(fechdesde, fechhasta)
            datartestadototalgeneral['tgciap']=rt.datosTotalGeneralConcluidoInasistenciaAmbasPartes(fechdesde, fechhasta)
            datartestadototalgeneral['tgcdmc']=rt.datosTotalGeneralConcluidoDesicionMotivaConciliador(fechdesde, fechhasta)
            datartestadototalgeneral['tgcci']=rt.datosTotalGeneralConcluidoInforme(fechdesde, fechhasta)
            datartestadototalgeneral['tgcti']=rt.datosTotalGeneralConcluidosTotal(fechdesde, fechhasta)
            dataestadototalgeneral.append(datartestadototalgeneral)
            datartestadototalgeneral={}
    
        try:
            template = get_template('reportes/rtrimestral/rtrimestralpdf.html')
            context = {
                'title': 'HOJA SUMARIA DEL SERVICIO CONCILIATORIO PRIVADO',
                'year': yearpdf,
                'periodo': self.kwargs['periodo'],
                'fechadesde': desde,
                'fechahasta': hasta,
                'datacivil': datacivil,
                'dataciviltotal': dataciviltotal,
                'datafamilia': datafamilia,
                'datafamiliatotal': datafamiliatotal,
                'dataestado': dataestado,
                'dataestadototal': dataestadototal,
                'dataestadototalgeneral': dataestadototalgeneral
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename = "Reporte Trimestral.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest = response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('ccjj:jj_reportetrimestral'))

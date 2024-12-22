from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from aplicaciones.ccjj.models import CajaConciliacion, Cliente, Procedimiento, Materia, Expediente, Socio
from aplicaciones.user.models import User
from django.contrib.auth.models import Group

from aplicaciones.ccjj.forms.conciliacion.materiaconciliacion.materiaconciliacion import MateriaConciliacionForm

from aplicaciones.ccjj.views.reportes.rporsocio.ReporteSocio import ReportePorSocio

from datetime import datetime, timedelta

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Create your views here.

class ReportePorSocioView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'reportes/rporsocio/rporsocio.html'
    form_class=MateriaConciliacionForm
    permission_required = 'view_acta'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchsocio':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Socio.objects.select_related('id_per').all():
                    data.append({'id': i.id, 'text': i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per})      
            elif action == 'searchmaterias':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Materia.objects.all():
                    data.append({'id': i.id, 'text': i.des_mat})
            elif action == 'search_procedimientos_id':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Procedimiento.objects.filter(id_mat_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.des_pro})    
            elif action == 'searchdatossocio':
                data = []
                idsoc = request.POST['id']
                if idsoc=='all':
                    data.append('Todos')
                    data.append('Todos')                    
                else:
                    for i in Socio.objects.select_related('id_per').filter(id=idsoc):
                        data.append(i.id_per.numdoc_per)
                        data.append(i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per)
            elif action == 'searchreportefiltro':
                # Mis Filtros
                socio=request.POST['socio']
                materia=request.POST['materia']
                procedimiento=request.POST['procedimiento']
                tipacta = request.POST['tipacta']
                fechdesde = datetime.strptime(request.POST['fechdesde'],'%Y-%m-%d')
                fechhasta = datetime.strptime(request.POST['fechhasta'],'%Y-%m-%d') + timedelta(days=1)

                data= []
                datarps={}

                rps=ReportePorSocio()
                
                # Para data expediente
                dataexp=''
                if socio == 'all': # Cuando son todos los socios
                    if materia == 'all': # Cuando son todas las materias
                        if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                            dataexp=Expediente.objects.filter(fec_exp__range=(fechdesde,fechhasta))
                        elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                            dataexp=Expediente.objects.filter(fec_exp__range=(fechdesde,fechhasta), estact_exp=tipacta)                        
                    elif materia != 'all': # Cuando se elige una materia
                        if procedimiento == 'all': # Cuando son todas los procedimientos de la materia
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta))
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta), estact_exp=tipacta)
                        elif procedimiento != 'all': # Cuando se elige un procedimiento
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta))
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta), estact_exp=tipacta)
                    
                    for e in dataexp:
                        datarps['numexp']=rps.numExpediente(e.id)
                        datarps['solicitante']=rps.datoSolicitantes(e.id)
                        datarps['invitado']=rps.datoInvitados(e.id)
                        datarps['fechsoli']=rps.datoFechaSolicitud(e.id)
                        datarps['materia']=rps.datoMateria(e.id)
                        datarps['procedimiento']=rps.datoProcedimiento(e.id)
                        datarps['numacta']=rps.datoNumActa(e.id)
                        datarps['numinforme']=rps.datoNumInforme(e.id)
                        datarps['tipacta_acta']=rps.datoTipoActa(e.id)
                        datarps['condecono']=rps.datoCondicionEconomica(e.id)
                        
                        data.append(datarps)
                        datarps={}
                                     
                elif socio != 'all': # Cuando se elige un socios
                    if materia == 'all': # Cuando son todas las materias
                        if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                            dataexp=CajaConciliacion.objects.filter(id_soc_id=socio, id_exp__fec_exp__range=(fechdesde,fechhasta))
                        elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                            dataexp=CajaConciliacion.objects.filter(id_soc_id=socio, id_exp__fec_exp__range=(fechdesde,fechhasta), id_exp__estact_exp=tipacta)                        
                    elif materia != 'all': # Cuando se elige una materia
                        if procedimiento == 'all': # Cuando son todos los procedimientos de la materia
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                dataexp=CajaConciliacion.objects.filter(id_soc_id=socio, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__fec_exp__range=(fechdesde,fechhasta))
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                dataexp=CajaConciliacion.objects.filter(id_soc_id=socio, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__fec_exp__range=(fechdesde,fechhasta), id_exp__estact_exp=tipacta)                                 
                        elif procedimiento != 'all': # Cuando se elige un procedimiento
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                dataexp=CajaConciliacion.objects.filter(id_soc_id=socio, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_exp__fec_exp__range=(fechdesde,fechhasta))
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                dataexp=CajaConciliacion.objects.filter(id_soc_id=socio, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_exp__fec_exp__range=(fechdesde,fechhasta), id_exp__estact_exp=tipacta)
             
                    for e in dataexp:
                        datarps['numexp']=rps.numExpediente(e.id_exp_id)
                        datarps['solicitante']=rps.datoSolicitantes(e.id_exp_id)
                        datarps['invitado']=rps.datoInvitados(e.id_exp_id)
                        datarps['fechsoli']=rps.datoFechaSolicitud(e.id_exp_id)
                        datarps['materia']=rps.datoMateria(e.id_exp_id)
                        datarps['procedimiento']=rps.datoProcedimiento(e.id_exp_id)
                        datarps['numacta']=rps.datoNumActa(e.id_exp_id)
                        datarps['numinforme']=rps.datoNumInforme(e.id_exp_id)
                        datarps['tipacta_acta']=rps.datoTipoActa(e.id_exp_id)
                        datarps['condecono']=rps.datoCondicionEconomica(e.id_exp_id)
                        
                        data.append(datarps)
                        datarps={}

            elif action == 'searchreporteall':
                
                data= []
                datarps={}

                rps=ReportePorSocio()

                for e in Expediente.objects.all():
                    
                    datarps['numexp']=rps.numExpediente(e.id)
                    datarps['solicitante']=rps.datoSolicitantes(e.id)
                    datarps['invitado']=rps.datoInvitados(e.id)
                    datarps['fechsoli']=rps.datoFechaSolicitud(e.id)
                    datarps['materia']=rps.datoMateria(e.id)
                    datarps['procedimiento']=rps.datoProcedimiento(e.id)
                    datarps['numacta']=rps.datoNumActa(e.id)
                    datarps['numinforme']=rps.datoNumInforme(e.id)
                    datarps['tipacta_acta']=rps.datoTipoActa(e.id)
                    datarps['condecono']=rps.datoCondicionEconomica(e.id)
                    
                    data.append(datarps)
                    datarps={}

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Por Socio'
        context['titleform']='REPORTE CONCILIACIONES POR SOCIOS'
        context['formmatcon'] = MateriaConciliacionForm()
       
        return context

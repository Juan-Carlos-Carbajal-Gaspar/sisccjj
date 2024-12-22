from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from aplicaciones.ccjj.models import Cliente, Procedimiento, Materia, Expediente
from aplicaciones.user.models import User
from django.contrib.auth.models import Group

from aplicaciones.ccjj.forms.conciliacion.materiaconciliacion.materiaconciliacion import MateriaConciliacionForm

from aplicaciones.ccjj.views.reportes.rporconciliador.ReporteConciliador import ReportePorConciliador

from datetime import datetime, timedelta

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin
# Create your views here.

class ReportePorConciliadorView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'reportes/rporconciliador/rporconciliador.html'
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
            if action == 'searchconciliador':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Group.objects.get(name="Conciliador").user_set.all():
                    data.append({'id': i.id, 'text': i.first_name + ' ' + i.last_name  })      
            elif action == 'searchmaterias':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Materia.objects.all():
                    data.append({'id': i.id, 'text': i.des_mat})
            elif action == 'search_procedimientos_id':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Procedimiento.objects.filter(id_mat_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.des_pro})    
            elif action == 'searchdatosconciliador':
                data = []
                idcon = request.POST['id']
                if idcon=='all':
                    data.append('Todos')
                    data.append('Todos')                    
                else:
                    for i in User.objects.filter(id=idcon):
                        data.append(i.dni_user)
                        data.append(i.first_name + ' ' + i.last_name)
            elif action == 'searchreportefiltro':
                # Mis Filtros
                conciliador=request.POST['conciliador']
                materia=request.POST['materia']
                procedimiento=request.POST['procedimiento']
                tipacta = request.POST['tipacta']
                fechdesde = datetime.strptime(request.POST['fechdesde'],'%Y-%m-%d')
                fechhasta = datetime.strptime(request.POST['fechhasta'],'%Y-%m-%d') + timedelta(days=1)

                data= []
                datarpc={}

                rpc=ReportePorConciliador()
                
                # Para data expediente
                dataexp=''
                if conciliador == 'all': # Cuando son todos los conciliadores
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
                        
                elif conciliador != 'all': # Cuando se elige un conciliador
                    if materia == 'all': # Cuando son todas las materias
                        if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                            dataexp=Expediente.objects.filter(id_user_id=conciliador, fec_exp__range=(fechdesde,fechhasta))
                        elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                            dataexp=Expediente.objects.filter(id_user_id=conciliador, fec_exp__range=(fechdesde,fechhasta), estact_exp=tipacta)
                    elif materia != 'all': # Cuando se elige una materia
                        if procedimiento == 'all': # Cuando son todos los procedimientos de la materia
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_user_id=conciliador, id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta))
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_user_id=conciliador, id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta), estact_exp=tipacta)    
                        elif procedimiento != 'all': # Cuando se elige un procedimiento
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_user_id=conciliador, id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta))
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(id_user_id=conciliador, id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta), estact_exp=tipacta)

                for e in dataexp:
                    datarpc['numexp']=rpc.numExpediente(e.id)
                    datarpc['solicitante']=rpc.datoSolicitantes(e.id)
                    datarpc['invitado']=rpc.datoInvitados(e.id)
                    datarpc['fechsoli']=rpc.datoFechaSolicitud(e.id)
                    datarpc['materia']=rpc.datoMateria(e.id)
                    datarpc['procedimiento']=rpc.datoProcedimiento(e.id)
                    datarpc['numacta']=rpc.datoNumActa(e.id)
                    datarpc['numinforme']=rpc.datoNumInforme(e.id)
                    datarpc['tipacta_acta']=rpc.datoTipoActa(e.id)
                    datarpc['condecono']=rpc.datoCondicionEconomica(e.id)
                    
                    data.append(datarpc)
                    datarpc={}

            elif action == 'searchreporteall':
                
                data= []
                datarpc={}

                rpc=ReportePorConciliador()

                for e in Expediente.objects.all():
                    
                    datarpc['numexp']=rpc.numExpediente(e.id)
                    datarpc['solicitante']=rpc.datoSolicitantes(e.id)
                    datarpc['invitado']=rpc.datoInvitados(e.id)
                    datarpc['fechsoli']=rpc.datoFechaSolicitud(e.id)
                    datarpc['materia']=rpc.datoMateria(e.id)
                    datarpc['procedimiento']=rpc.datoProcedimiento(e.id)
                    datarpc['numacta']=rpc.datoNumActa(e.id)
                    datarpc['numinforme']=rpc.datoNumInforme(e.id)
                    datarpc['tipacta_acta']=rpc.datoTipoActa(e.id)
                    datarpc['condecono']=rpc.datoCondicionEconomica(e.id)
                    
                    data.append(datarpc)
                    datarpc={}

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Por Conciliador'
        context['titleform']='REPORTE CONCILIACIONES POR CONCILIADOR'
        context['formmatcon'] = MateriaConciliacionForm()
       
        return context

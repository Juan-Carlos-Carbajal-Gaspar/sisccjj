from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from aplicaciones.ccjj.models import Cliente, Invitado, Procedimiento, Materia, Expediente, Solicitante, Persona
from aplicaciones.user.models import User
from django.contrib.auth.models import Group

from aplicaciones.ccjj.forms.conciliacion.materiaconciliacion.materiaconciliacion import MateriaConciliacionForm

from aplicaciones.ccjj.views.reportes.rporcliente.ReporteCliente import ReportePorCliente

from datetime import datetime, timedelta

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin
# Create your views here.

class ReportePorClienteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):

    template_name = 'reportes/rporcliente/rporcliente.html'
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

            if action == 'search_cliente_tip':

                data = [{'id': 'all', 'text': 'Todos'}]
                tipcli = request.POST.get('tipcli')

                if tipcli == 'all':
                    for cli in Cliente.objects.select_related('id_per').all():
                        data.append({'id': cli.id_per.id, 'text': cli.id_per.nom_per + ' ' + cli.id_per.apepat_per + ' ' + cli.id_per.apemat_per})      
                        
                elif tipcli == 's':
                    datacli=[]
                    for i in Solicitante.objects.select_related('id_per').all():
                        if i.id_per_id not in datacli:
                            datacli.append(i.id_per_id)
                    for dcli in datacli:
                        for ds in Cliente.objects.select_related('id_per').filter(id_per = dcli):
                            data.append({'id': ds.id_per.id, 'text': ds.id_per.nom_per+ ' ' + ds.id_per.apepat_per + ' ' + ds.id_per.apemat_per})      
                elif tipcli == 'i':
                    datacli=[]
                    for i in Invitado.objects.select_related('id_per').all():
                        if i.id_per_id not in datacli:
                            datacli.append(i.id_per_id)
                    for dcli in datacli:
                        for di in Cliente.objects.select_related('id_per').filter(id_per = dcli):
                            data.append({'id': di.id_per.id, 'text': di.id_per.nom_per+ ' ' + di.id_per.apepat_per + ' ' + di.id_per.apemat_per})      
                         
            elif action == 'searchmaterias':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Materia.objects.all():
                    data.append({'id': i.id, 'text': i.des_mat})
            elif action == 'search_procedimientos_id':
                data = [{'id': 'all', 'text': 'Todos'}]
                for i in Procedimiento.objects.filter(id_mat_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.des_pro})    
            elif action == 'searchdatoscliente':
                data = []
                idcli = request.POST['id']
                if idcli=='all':
                    data.append('Todos')
                    data.append('Todos')                    
                else:
                    for i in Persona.objects.filter(id=idcli):
                        data.append(i.numdoc_per)
                        data.append(i.nom_per + ' ' + i.apepat_per + ' ' + i.apemat_per)            
            elif action == 'searchreportefiltro':
                # Mis Filtros
                tipcliente=request.POST['tipcliente']
                cliente=request.POST['cliente']
                materia=request.POST['materia']
                procedimiento=request.POST['procedimiento']
                tipacta = request.POST['tipacta']
                fechdesde = datetime.strptime(request.POST['fechdesde'],'%Y-%m-%d')
                fechhasta = datetime.strptime(request.POST['fechhasta'],'%Y-%m-%d') + timedelta(days=1)

                data= []
                datarpc={}

                rpc=ReportePorCliente()
                
                # Para data expediente
                datacliexp=''

                if tipcliente == 'all': # Cuando son todos los tipos de clientes
                    if cliente == 'all': # Cuando son todos los clientes
                        dataexp=''
                        if materia == 'all': # Cuando son todas las materias
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(fec_exp__range=(fechdesde,fechhasta))
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                dataexp=Expediente.objects.filter(estact_exp=tipacta, fec_exp__range=(fechdesde,fechhasta))
                        elif materia != 'all': # Cuando se elige una materia
                            if procedimiento == 'all': # Cuando son todas los procedimientos de la materia
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    dataexp=Expediente.objects.filter(id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta))
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    dataexp=Expediente.objects.filter(estact_exp=tipacta, id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta))                                
                            elif procedimiento != 'all': # Cuando se elige un procedimiento
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    dataexp=Expediente.objects.filter(id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta))
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    dataexp=Expediente.objects.filter(estact_exp=tipacta, id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta))
                                
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
                            
                    elif cliente != 'all': # Cuando no son todos los clientes
                        ##### Agrupamos Tabla Solicitante e Invitado
                        datacliente=[]
                        for i in Solicitante.objects.select_related().filter(id_per = cliente):
                            datacliente.append(i.id_exp_id)
                        for i in Invitado.objects.select_related().filter(id_per = cliente):
                            datacliente.append(i.id_exp_id)
                        ##### Agrupamos Tabla Solicitante e Invitados

                        if materia == 'all': # Cuando son todas las materias
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)   
                                datasolinv = {}
                                for dsi in datacliente:
                                    for e in Expediente.objects.filter(id = dsi, fec_exp__range=(fechdesde,fechhasta)):
                                        datasolinv['numexp']=rpc.numExpediente(e.id)
                                        datasolinv['solicitante']=rpc.datoSolicitantes(e.id)
                                        datasolinv['invitado']=rpc.datoInvitados(e.id)
                                        datasolinv['fechsoli']=rpc.datoFechaSolicitud(e.id)
                                        datasolinv['materia']=rpc.datoMateria(e.id)
                                        datasolinv['procedimiento']=rpc.datoProcedimiento(e.id)
                                        datasolinv['numacta']=rpc.datoNumActa(e.id)
                                        datasolinv['numinforme']=rpc.datoNumInforme(e.id)
                                        datasolinv['tipacta_acta']=rpc.datoTipoActa(e.id)
                                        datasolinv['condecono']=rpc.datoCondicionEconomica(e.id)
                                            
                                        data.append(datasolinv)
                                        datasolinv={}
                                
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                datasolinv = {}
                                for dsi in datacliente:
                                    for e in Expediente.objects.filter(id = dsi, estact_exp=tipacta, fec_exp__range=(fechdesde,fechhasta)):
                                        datasolinv['numexp']=rpc.numExpediente(e.id)
                                        datasolinv['solicitante']=rpc.datoSolicitantes(e.id)
                                        datasolinv['invitado']=rpc.datoInvitados(e.id)
                                        datasolinv['fechsoli']=rpc.datoFechaSolicitud(e.id)
                                        datasolinv['materia']=rpc.datoMateria(e.id)
                                        datasolinv['procedimiento']=rpc.datoProcedimiento(e.id)
                                        datasolinv['numacta']=rpc.datoNumActa(e.id)
                                        datasolinv['numinforme']=rpc.datoNumInforme(e.id)
                                        datasolinv['tipacta_acta']=rpc.datoTipoActa(e.id)
                                        datasolinv['condecono']=rpc.datoCondicionEconomica(e.id)
                                            
                                        data.append(datasolinv)
                                        datasolinv={}

                        elif materia != 'all': # Cuando se elige una materia
                            if procedimiento == 'all': # Cuando son todas los procedimientos de la materia
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datasolinv = {}
                                    for dsi in datacliente:
                                        for e in Expediente.objects.filter(id = dsi, id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta)):
                                            datasolinv['numexp']=rpc.numExpediente(e.id)
                                            datasolinv['solicitante']=rpc.datoSolicitantes(e.id)
                                            datasolinv['invitado']=rpc.datoInvitados(e.id)
                                            datasolinv['fechsoli']=rpc.datoFechaSolicitud(e.id)
                                            datasolinv['materia']=rpc.datoMateria(e.id)
                                            datasolinv['procedimiento']=rpc.datoProcedimiento(e.id)
                                            datasolinv['numacta']=rpc.datoNumActa(e.id)
                                            datasolinv['numinforme']=rpc.datoNumInforme(e.id)
                                            datasolinv['tipacta_acta']=rpc.datoTipoActa(e.id)
                                            datasolinv['condecono']=rpc.datoCondicionEconomica(e.id)
                                                
                                            data.append(datasolinv)
                                            datasolinv={}

                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datasolinv = {}
                                    for dsi in datacliente:
                                        for e in Expediente.objects.filter(id = dsi, estact_exp=tipacta, id_esp__id_pro__id_mat_id=materia, fec_exp__range=(fechdesde,fechhasta)):
                                            datasolinv['numexp']=rpc.numExpediente(e.id)
                                            datasolinv['solicitante']=rpc.datoSolicitantes(e.id)
                                            datasolinv['invitado']=rpc.datoInvitados(e.id)
                                            datasolinv['fechsoli']=rpc.datoFechaSolicitud(e.id)
                                            datasolinv['materia']=rpc.datoMateria(e.id)
                                            datasolinv['procedimiento']=rpc.datoProcedimiento(e.id)
                                            datasolinv['numacta']=rpc.datoNumActa(e.id)
                                            datasolinv['numinforme']=rpc.datoNumInforme(e.id)
                                            datasolinv['tipacta_acta']=rpc.datoTipoActa(e.id)
                                            datasolinv['condecono']=rpc.datoCondicionEconomica(e.id)
                                                
                                            data.append(datasolinv)
                                            datasolinv={}

                            elif procedimiento != 'all': # Cuando se elige un procedimiento
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datasolinv = {}
                                    for dsi in datacliente:
                                        for e in Expediente.objects.filter(id = dsi, id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta)):
                                            datasolinv['numexp']=rpc.numExpediente(e.id)
                                            datasolinv['solicitante']=rpc.datoSolicitantes(e.id)
                                            datasolinv['invitado']=rpc.datoInvitados(e.id)
                                            datasolinv['fechsoli']=rpc.datoFechaSolicitud(e.id)
                                            datasolinv['materia']=rpc.datoMateria(e.id)
                                            datasolinv['procedimiento']=rpc.datoProcedimiento(e.id)
                                            datasolinv['numacta']=rpc.datoNumActa(e.id)
                                            datasolinv['numinforme']=rpc.datoNumInforme(e.id)
                                            datasolinv['tipacta_acta']=rpc.datoTipoActa(e.id)
                                            datasolinv['condecono']=rpc.datoCondicionEconomica(e.id)
                                                
                                            data.append(datasolinv)
                                            datasolinv={}

                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datasolinv = {}
                                    for dsi in datacliente:
                                        for e in Expediente.objects.filter(id = dsi, estact_exp=tipacta, id_esp__id_pro__id_mat_id=materia, id_esp__id_pro_id=procedimiento, fec_exp__range=(fechdesde,fechhasta)):
                                            datasolinv['numexp']=rpc.numExpediente(e.id)
                                            datasolinv['solicitante']=rpc.datoSolicitantes(e.id)
                                            datasolinv['invitado']=rpc.datoInvitados(e.id)
                                            datasolinv['fechsoli']=rpc.datoFechaSolicitud(e.id)
                                            datasolinv['materia']=rpc.datoMateria(e.id)
                                            datasolinv['procedimiento']=rpc.datoProcedimiento(e.id)
                                            datasolinv['numacta']=rpc.datoNumActa(e.id)
                                            datasolinv['numinforme']=rpc.datoNumInforme(e.id)
                                            datasolinv['tipacta_acta']=rpc.datoTipoActa(e.id)
                                            datasolinv['condecono']=rpc.datoCondicionEconomica(e.id)
                                                
                                            data.append(datasolinv)
                                            datasolinv={}
                    
                elif tipcliente == 's': # Cuando se elige un tipo de cliente como Solicitante
                    datavalidar=[]
                    if cliente == 'all': # Cuando son todos los clientes
                        if materia == 'all': # Cuando son todas las materias
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                datacliexp = Solicitante.objects.select_related().filter(id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                datacliexp = Solicitante.objects.select_related().filter(id_exp__estact_exp = tipacta, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                        elif materia != 'all': # Cuando se elige una materia
                            if procedimiento == 'all': # Cuando son todas los procedimientos de la materia
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__fec_exp__range=(fechdesde,fechhasta))
                            elif procedimiento != 'all': # Cuando se elige un procedimiento
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_exp__fec_exp__range=(fechdesde,fechhasta))                                                
                    elif cliente != 'all': # Cuando no son todos los clientes
                        if materia == 'all': # Cuando son todas las materias
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                datacliexp = Solicitante.objects.select_related().filter(id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                datacliexp = Solicitante.objects.select_related().filter(id_exp__estact_exp = tipacta, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                        elif materia != 'all': # Cuando se elige una materia
                            if procedimiento == 'all': # Cuando son todas los procedimientos de la materia
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))
                            elif procedimiento != 'all': # Cuando se elige un procedimiento
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Solicitante.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                                                
                    
                    for e in datacliexp:
                        if e.id_exp_id not in datavalidar:
                            datavalidar.append(e.id_exp_id)
                            datarpc['numexp']=rpc.numExpediente(e.id_exp_id)
                            datarpc['solicitante']=rpc.datoSolicitantes(e.id_exp_id)
                            datarpc['invitado']=rpc.datoInvitados(e.id_exp_id)
                            datarpc['fechsoli']=rpc.datoFechaSolicitud(e.id_exp_id)
                            datarpc['materia']=rpc.datoMateria(e.id_exp_id)
                            datarpc['procedimiento']=rpc.datoProcedimiento(e.id_exp_id)
                            datarpc['numacta']=rpc.datoNumActa(e.id_exp_id)
                            datarpc['numinforme']=rpc.datoNumInforme(e.id_exp_id)
                            datarpc['tipacta_acta']=rpc.datoTipoActa(e.id_exp_id)
                            datarpc['condecono']=rpc.datoCondicionEconomica(e.id_exp_id)
                                
                            data.append(datarpc)
                            datarpc={}
                            
                    datavalidar=[]
                elif tipcliente == 'i': # Cuando se elige un tipo de cliente como Invitado
                    datavalidar=[]
                    if cliente == 'all': # Cuando son todos los clientes
                        if materia == 'all': # Cuando son todas las materias
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                datacliexp = Invitado.objects.select_related().filter(id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                datacliexp = Invitado.objects.select_related().filter(id_exp__estact_exp = tipacta, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                        elif materia != 'all': # Cuando se elige una materia
                            if procedimiento == 'all': # Cuando son todas los procedimientos de la materia
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__fec_exp__range=(fechdesde,fechhasta))
                            elif procedimiento != 'all': # Cuando se elige un procedimiento
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_exp__fec_exp__range=(fechdesde,fechhasta))                                                
                    elif cliente != 'all': # Cuando no son todos los clientes
                        if materia == 'all': # Cuando son todas las materias
                            if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                datacliexp = Invitado.objects.select_related().filter(id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                            elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                datacliexp = Invitado.objects.select_related().filter(id_exp__estact_exp = tipacta, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                        elif materia != 'all': # Cuando se elige una materia
                            if procedimiento == 'all': # Cuando son todas los procedimientos de la materia
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))
                            elif procedimiento != 'all': # Cuando se elige un procedimiento
                                if tipacta == 'all': # Cuando son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                    
                                elif tipacta != 'all': # Cuando no son todas las actas (Concluido y no Concluido)
                                    datacliexp = Invitado.objects.select_related().filter(id_exp__estact_exp=tipacta, id_exp__id_esp__id_pro__id_mat_id=materia, id_exp__id_esp__id_pro_id=procedimiento, id_per=cliente, id_exp__fec_exp__range=(fechdesde,fechhasta))                                                
                    
                    for e in datacliexp:
                        if e.id_exp_id not in datavalidar:
                            datavalidar.append(e.id_exp_id)
                            datarpc['numexp']=rpc.numExpediente(e.id_exp_id)
                            datarpc['solicitante']=rpc.datoSolicitantes(e.id_exp_id)
                            datarpc['invitado']=rpc.datoInvitados(e.id_exp_id)
                            datarpc['fechsoli']=rpc.datoFechaSolicitud(e.id_exp_id)
                            datarpc['materia']=rpc.datoMateria(e.id_exp_id)
                            datarpc['procedimiento']=rpc.datoProcedimiento(e.id_exp_id)
                            datarpc['numacta']=rpc.datoNumActa(e.id_exp_id)
                            datarpc['numinforme']=rpc.datoNumInforme(e.id_exp_id)
                            datarpc['tipacta_acta']=rpc.datoTipoActa(e.id_exp_id)
                            datarpc['condecono']=rpc.datoCondicionEconomica(e.id_exp_id)
                                
                            data.append(datarpc)
                            datarpc={}
                            
                    datavalidar=[]
                
            elif action == 'searchreporteall':
                
                data= []
                datarpc={}

                rpc=ReportePorCliente()

                for e in Expediente.objects.all().order_by('-id'):
             
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
        context['title'] = 'Reporte Por Cliente'
        context['titleform']='REPORTE CONCILIACIONES POR CLIENTES'
        context['formmatcon'] = MateriaConciliacionForm()
       
        return context
# 
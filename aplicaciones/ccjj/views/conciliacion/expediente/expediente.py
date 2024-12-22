import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

# IMPORTANDON CLASES CRUD DE DJANGO
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

# IMPORTANDO CLASE EXPEDIENTEDATOS
from aplicaciones.ccjj.views.conciliacion.expediente.expedientedatos import ExpedienteDatos
# IMPORTANDO MODELO EXPEDIENTE
from aplicaciones.ccjj.models import Agenda, CajaConciliacion, Periodo, Expediente, Solicitud, Informe
from aplicaciones.user.models import User
# from django.contrib.auth.models import User
# IMPORTANDO FORM EXPEDIENTE
from aplicaciones.ccjj.forms.conciliacion.expediente.expediente import ExpedienteForm

from datetime import date
from datetime import datetime
# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin

# Create your views here.

# Listar Expedientes
class ListaExpediente(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Expediente
    template_name = "conciliacion/expediente/listaexpediente.html"
    permission_required = 'view_expediente'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'listaexpediente':
                data = []
                dataconsulta=''
                if request.user.id == 1:
                    dataconsulta = Expediente.objects.all().order_by('-id')
                else:
                    dataconsulta = Expediente.objects.filter(id_user =request.user.id).order_by('-id')
                for i in dataconsulta:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Expedientes'
        context['titleform']='EXPEDIENTES REGISTRADOS'
        context['list_url']=reverse_lazy('ccjj:jj_listaexpediente')
    
        return context
       
class CrearExpediente(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    
    model = Expediente
    form_class = ExpedienteForm
    template_name = 'conciliacion/expediente/crearexpediente.html'
    success_url = reverse_lazy('ccjj:jj_listaexpediente')
    permission_required = 'add_expediente'
        
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'crearexpediente':
                                
                expdat=ExpedienteDatos()
                
                # Guardar datos de Expediente
                exp=Expediente()
                exp.num_exp=expdat.numexp()
                exp.fec_exp=expdat.fecha()
                exp.hor_exp=expdat.hora()
                exp.proini_exp='EN PROCEDIMIENTO'
                exp.esttra_exp='EN TRAMITE'
                exp.estact_exp=''
                exp.audact_exp='SI'
                exp.numfol_exp=0
                exp.confin_exp='NO FINALIZADO'
                exp.inv_exp=''
                exp.tipcon_exp=request.POST['tipcon_exp']

                # Consultamos id expediente
                for i in Periodo.objects.filter(est_pe='a'):
                    idc=i.id

                exp.id_pe_id=idc
                exp.id_esp_id=1

                # Consultamos id Usuario
                exp.id_user_id=request.user.id
                exp.estpro_exp='exp'
                exp.save()

                # Actualizamos Tabla Configuracion
                conf=Periodo.objects.get(est_pe="a")
                conf.num_exp=int(expdat.numexp()) + 1
                conf.save()
                                
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Expediente'
        context['titleform']='Nuevo Expediente'
        context['action'] = 'crearexpediente'
        context['tipoaction'] = 'add'
        context['read_url'] = self.success_url
               
        return context
 
class ListaExpedienteDetalle(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Expediente
    template_name = "conciliacion/expediente/listaexpedientedetalle.html"
    # permission_required = 'view_expediente'
    permission_required = 'view_expediente', 'change_expediente', 'add_expediente'

    
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            fechaactual = datetime.now()
                                 
            if action == 'listaexpedientedetalle':
                dataexp=[]
                dataexpediente = {}
                idexp=self.kwargs.get('pk')

                for i in Expediente.objects.filter(pk=idexp):
                    dataexpediente['id'] = idexp
                    dataexpediente['numexp'] = i.num_exp
                    dataexpediente['fecha'] = i.fec_exp
                    dataexpediente['hora'] = i.hor_exp
                    dataexpediente['tipcon'] = i.tipcon_exp
                        
                    if Solicitud.objects.filter(id_exp=idexp).count() > 0:
                        dataexpediente['solicitud']='exisol'
                    else:
                        dataexpediente['solicitud'] = 'gensol'

                    dataexpediente['idusuario'] = request.user.id

                    if CajaConciliacion.objects.filter(id_exp=idexp).count() > 0:
                        dataexpediente['exicaja']=1
                    else:
                        dataexpediente['exicaja']=0

                    if Informe.objects.filter(id_exp=idexp).count() > 0:
                        dataexpediente['exiacta'] = 1
                    else:
                        dataexpediente['exiacta'] = 0

                    dataexpediente['estpro'] = i.estpro_exp
                    dataexpediente['fechaactual'] =fechaactual.strftime("%Y-%m-%d")

                    for fecaud in Agenda.objects.filter(id_exp=idexp):
                        fechaudiencia =fecaud.fecaud_age
                        dataexpediente['fechaaudiencia']=fechaudiencia.strftime("%Y-%m-%d")
                                        
                    dataexp.append(dataexpediente)
                    dataexpediente={}

                data = dataexp
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expdatos = ExpedienteDatos()
        context['title'] = 'Expediente N°: ' + str(expdatos.numexpYear(self.kwargs.get('pk')))
        context['titleform']='Expediente N°: ' + str(expdatos.numexpYear(self.kwargs.get('pk')))
        context['list_url']=reverse_lazy('ccjj:jj_listaexpediente')    
        return context
 
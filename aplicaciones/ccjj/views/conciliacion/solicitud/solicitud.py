import json
import io
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt, csrf_protect

# IMPORTANDON CLASES CRUD DE DJANGO
from django.views.generic import CreateView 
from django.utils.decorators import method_decorator
from django.db import transaction

# IMPORTANDO CLASE SOLICITUDDATOS
from aplicaciones.ccjj.views.conciliacion.solicitud.solicituddatos import SolicitudDatos
# IMPORTANDO MODELOS
from aplicaciones.ccjj.models import Documento, Expediente, Invitado, Persona, Solicitante, Solicitud, Cliente

# IMPORTANDO FORM SOLICITUD
from aplicaciones.ccjj.forms.conciliacion.solicitud.solicitud import SolicitudForm
# IMPORTANDO FORM CLIENTE
from aplicaciones.ccjj.forms.cliente.cliente import ClienteForm

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
class CrearSolicitud(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'conciliacion/solicitud/crearsolicitud.html'
    permission_required = 'add_solicitud'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # Para buscar solicitante e invitado
            if action == 'search_cliente':
                data = []
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})

                cli = Cliente.objects.select_related('id_per').filter(id_per__numdoc_per__icontains=term)
                for i in cli[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
                    
            # Para crear un nuevo Cliente
            elif action == 'create_cliente':
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

                cli=Cliente()
                cli.id_per_id=per.id
                cli.save()    
            # Editar datos del Cliente
            elif action == 'editar_cliente':
                per= Persona.objects.get(pk=request.POST['id'])
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
            # Para crear la solicitud
            elif action == 'crearsolicitud':
                # Clase Solicitud
                soldoc=SolicitudDatos()
                
                with transaction.atomic():
                    idexp=self.kwargs.get('pk')
                    expdatos=SolicitudDatos()

                    # Capturar datos para solicitud
                    sol=Solicitud()
                    sol.fecdoc_sol=expdatos.fecha()
                    sol.hecdoc_sol=request.POST['txtHechos']
                    sol.pretsoldoc_sol='Por medio de la conciliación es nuestra pretensión fijar ' + request.POST['txtPretension']
                    sol.pretactdoc_sol='Por medio de la conciliación es pretension de las partes fijar ' + request.POST['txtPretension']
                    sol.id_exp_id=idexp
                    sol.save()

                    # Capturar datos de solicitantes
                    soli = json.loads(request.POST['solicitante'])
                    for i in soli['solicitantes']:
                        solexp=Solicitante()
                        solexp.id_per_id=i['id_per']
                        solexp.id_exp_id = idexp
                        solexp.save()

                    # Capturar datos de invitados
                    inv = json.loads(request.POST['invitado'])
                    for i in inv['invitados']:
                        invexp=Invitado()
                        invexp.id_per_id=i['id_per']
                        invexp.id_exp_id = idexp
                        invexp.save()
                    
                    # Agregamos Documento Solicitud
                    docsol = Documento()
                    docsol.tip_doc = 'SOLICITUD DEL EXPEDIENTE N° ' + str(soldoc.numSolicitud(idexp)) + '-' + soldoc.year()
                    docsol.arcesc_doc = ''
                    docsol.t_doc = 'solicitud'
                    docsol.id_exp_id = idexp
                    docsol.save()

                    # Actualizamos Expediente
                    exp = Expediente.objects.get(pk=idexp)
                    exp.estpro_exp='sol'
                    exp.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        expdatos=SolicitudDatos()
        idexp=self.kwargs.get('pk')

        context['title'] = 'Solicitud de Conciliación'
        context['titleform'] = 'Solicitud de Conciliación'
        context['action'] = 'crearsolicitud'
        context['tipoaction'] = 'add'
        context['idexpediente'] = idexp
        context['tipcform'] = expdatos.tipoConciliacion(idexp)
        context['numsol'] = expdatos.numSolicitud(idexp)
        context['fechahora'] = expdatos.fecha()
        context['formcliente'] = ClienteForm()

        return context

# Generar Solicitud Word
def generarSolicitud(self, pk):
    idexp=pk
    # Clase Solicitud
    soldoc=SolicitudDatos()

    fecha=datetime.now()
    docsolicitud = DocxTemplate('plantillasdoc/plantillasolicitud.docx')
    context={
        'numsol': soldoc.numSolicitud(idexp),
        'year': soldoc.yearSolicitud(idexp),
        'terminosolicitante': soldoc.terminoSolicitante(idexp),
        'solicitantes': soldoc.datosSolicitantes(idexp),
        'terminoinicio': soldoc.datosTerminoInicio(idexp),
        'hechos': soldoc.datoHechos(idexp),
        'pretension': soldoc.datoPretension(idexp),
        'terminoinvitacion': soldoc.terminoInvitacion(idexp),
        'terminoinvitado': soldoc.terminoInvitado(idexp),
        'invitados': soldoc.datosInvitados(idexp),
        'terminodni': soldoc.terminoDni(idexp),
        'fechasol': 'Huancayo, ' + fecha.strftime("%d de %B del año " + soldoc.year())
    }
    docsolicitud.render(context)

    document_data = io.BytesIO()
    docsolicitud.save(document_data)
    document_data.seek(0)
    response = HttpResponse(document_data.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    response["Content-Disposition"] = 'attachment; filename = "Solicitud Expediente N° '+ str(soldoc.numSolicitud(idexp)+ '-' + soldoc.year()) +'.docx"'
    response["Content-Encoding"] = "UTF-8"
    
    return response
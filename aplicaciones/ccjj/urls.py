from django.contrib import admin
from django.urls import path

# Importando Clase Iniciar Sesion
from aplicaciones.ccjj.views.dashboard.dashboard import DashboardView
# Importando Clase Iniciar Sesion
from aplicaciones.ccjj.views.iniciarsesion.iniciarsesion import *
# Importando Clase ListaPeriodo
from aplicaciones.ccjj.views.periodo.periodo import *
# Importando Clase Cliente
from aplicaciones.ccjj.views.cliente.cliente import *
# Importando Clase Materia
from aplicaciones.ccjj.views.materia.materia import *
# Importando Clase Procedimiento
from aplicaciones.ccjj.views.procedimiento.procedimiento import *
# Importando Clase Especificacion
from aplicaciones.ccjj.views.especificacion.especificacion import *
# Importando Clase Socio
from aplicaciones.ccjj.views.socio.socio import *
# Importando Clase Expediente
from aplicaciones.ccjj.views.conciliacion.expediente.expediente import *
# Importando Clase Solicitud
from aplicaciones.ccjj.views.conciliacion.solicitud.solicitud import *
# Importando Clase Materia Conciliacion
from aplicaciones.ccjj.views.conciliacion.materiaconciliacion.materiaconciliacion import *
# Importando Clase Esquela Conciliacion
from aplicaciones.ccjj.views.conciliacion.esquelaconciliador.esquelaconciliador import *
# Importando Clase Invitacion Conciliacion
from aplicaciones.ccjj.views.conciliacion.invitacion.invitacion import *
# Importando Clase Pago Conciliacion
from aplicaciones.ccjj.views.conciliacion.ingresoconciliacion.ingresoconciliacion import *
# Importando Clase de Acta Conciliacion
from aplicaciones.ccjj.views.conciliacion.actaconciliacion.actaconciliacion import *
# Importando Clase de Documentos Conciliacion
from aplicaciones.ccjj.views.conciliacion.documentos.documentos import *

# Importando Clase de Reporte Trimestral
from aplicaciones.ccjj.views.reportes.rtrimestral.rtrimestral import *
# Importando Clase de Reporte POr Cliente
from aplicaciones.ccjj.views.reportes.rporcliente.rporcliente import *
# Importando Clase de Reporte POr Socio
from aplicaciones.ccjj.views.reportes.rporsocio.rporsocio import *
# Importando Clase de Reporte Por Conciliador
from aplicaciones.ccjj.views.reportes.rporconciliador.rporconciliador import *
# Importando Clase de Reporte Financiero
from aplicaciones.ccjj.views.reportes.rfinanciero.rfinanciero import *

# Nombre de la URL
app_name = 'ccjj'

urlpatterns = [
    # Iniciar Sesion
    path('',IniciarSesionFormView.as_view(), name='jj_iniciarsesion'),
    # Cerrar Sesion
    path('logout/', CerrarSesionFormView.as_view(), name='jj_cerrarsesion'),
    # Dashboard
    path('dashboard/',DashboardView.as_view(), name='jj_dashboard'),

    # Materia
    path('materia/',ListaMateria.as_view(), name='jj_listamateria'),
    path('materia/crearmateria/',CrearMateria.as_view(), name='jj_crearmateria'),
    path('materia/editarmateria/<int:pk>/',EditarMateria.as_view(), name='jj_editarmateria'),

    # Procedimiento
    path('procedimiento/',ListaProcedimiento.as_view(), name='jj_listaprocedimiento'),
    path('procedimiento/crearprocedimiento/',CrearProcedimiento.as_view(), name='jj_crearprocedimiento'),
    path('procedimiento/editarprocedimiento/<int:pk>/',EditarProcedimiento.as_view(), name='jj_editarprocedimiento'),

    # Especificacion
    path('especificacion/',ListaEspecificacion.as_view(), name='jj_listaespecificacion'),
    path('especificacion/crearespecificacion/',CrearEspecificacion.as_view(), name='jj_crearespecificacion'),
    path('especificacion/editarespecificacion/<int:pk>/',EditarEspecificacion.as_view(), name='jj_editarespecificacion'),

    # Cliente
    path('cliente/',ListaCliente.as_view(), name='jj_listacliente'),
    path('cliente/crearcliente/',CrearCliente.as_view(), name='jj_crearcliente'),
    path('cliente/editarcliente/<int:pk>/',EditarCliente.as_view(), name='jj_editarcliente'),

    # Periodo
    path('periodo/',ListaPeriodo.as_view(), name='jj_listaperiodo'),
    path('periodo/crearperiodo/',CrearPeriodo.as_view(), name='jj_crearperiodo'),
    path('periodo/editarperiodo/<int:pk>/',EditarPeriodo.as_view(), name='jj_editarperiodo'),

    # Socio
    path('socio/',ListaSocio.as_view(), name='jj_listasocio'),
    path('socio/crearsocio/',CrearSocio.as_view(), name='jj_crearsocio'),
    path('socio/editarsocio/<int:pk>/',EditarSocio.as_view(), name='jj_editarsocio'),    
    path('socio/eliminarsocio/<int:pk>/',EliminarSocio.as_view(), name='jj_eliminarsocio'),

    # Expediente
    path('expediente/',ListaExpediente.as_view(), name='jj_listaexpediente'),
    path('expediente/crearexpediente/',CrearExpediente.as_view(), name='jj_crearexpediente'),
    path('expediente/expedientedetalle/<int:pk>/', ListaExpedienteDetalle.as_view(), name='jj_listaexpedientedetalle'),
    path('expediente/expedientesolicitud/<int:pk>/', CrearSolicitud.as_view(), name='jj_crearsolicitud'),
    # Plantilla Solicitud
    path('gensolicitud/<int:pk>/', generarSolicitud, name='jj_generarsolicitud'),
    path('expediente/expedientemateriaconciliacion/<int:pk>/', SeleccionarMateriaConciliacion.as_view(), name='jj_crearmateriaconciliacion'),
    path('expediente/expedienteesquelaconciliador/<int:pk>/', CrearEsquelaConciliador.as_view(), name='jj_crearesquelaconciliador'),
    # Plantilla Esquela Conciliador
    path('genesquelaconciliador/<int:pk>/', generarEsquelaConciliador, name='jj_generaresquelaconciliador'),
    path('expediente/expedientepago/<int:pk>/', CrearIngresoConciliacionView.as_view(), name='jj_crearingresoconciliacion'),
    path('expediente/cajaconciliacion/<int:pk>/', CajaConciliacionView.as_view(), name='jj_cajaconciliacion'),
    
    path('expediente/invitacion/<int:pk>/', CrearInvitaciónConciliacionView.as_view(), name='jj_crearinvitacionconciliacion'),
    # Primera Invitacion
    path('genpriinvitacion/<int:pk>/<int:id>/<str:fecha>/', generarPrimeraInvitacion, name='jj_generarprimerainvitacion'),
    # Segunda Invitacion
    path('genseginvitacion/<int:pk>/<int:id>/<str:fecha>/', generarSegundaInvitacion, name='jj_generarsegundainvitacion'),
    # Acta de Conciliacion
    path('genactaconciliacion/<int:pk>/', CrearActaConciliacion.as_view(), name='jj_generaractaconciliacion'),
    # Plantilla Acta Conciliacion
    path('generaracta/<int:pk>/', generarActa, name='jj_generaractaconciliacion'),
    
    # Lista Documentos de Conciliacion}
    path('listadocumentos/<int:pk>/', ListaDocumentos.as_view(), name='jj_listadocumentos'),

    # Recibo de Ingresos Conciliacion / Ingreso copias
    path('genreciboingresos/<int:pk>/', generarRecibo, name='jj_genreciboingresos'),
    path('genreciboingresoscopias/<int:pk>/', generarReciboCopias, name='jj_genreciboingresoscopias'),

    # Reportes
    #path('reporte/trimestral/', ListaDocumentos.as_view(), name='jj_reportetrimestral'),
    # Reporte Trimestral
    path('reportetrimestral/', ReporteTrimestralView.as_view(), name='jj_reportetrimestral'),
    # Reporte Trimestral Invoice PDF
    path('reportetrimestralpdf/<int:year>/<str:periodo>/<str:fechadesde>/<str:fechahasta>/', ReporteTrimestralInvoicePdf.as_view(), name='jj_reportetrimestralinvoicepdf'),
    # Reporte Por Cliente
    path('reporteporcliente/', ReportePorClienteView.as_view(), name='jj_reporteporcliente'),
    # Reporte Por Socio
    path('reporteporsocio/', ReportePorSocioView.as_view(), name='jj_reporteporsocio'),
    # Reporte Por Socio
    path('reporteporconciliador/', ReportePorConciliadorView.as_view(), name='jj_reporteporconciliador'),
    # Reporte Financiero
    path('reportefinanciero/', ReporteFinancieroView.as_view(), name='jj_reportefinanciero'),
    
    
]

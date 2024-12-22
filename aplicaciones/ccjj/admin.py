from django.contrib import admin
# Importando Modelos
from .models import *
from aplicaciones.user.models import User as Usuario

# Register your models here.
# class UsuarioAdmin(admin.ModelAdmin):
# 	list_display=['id', 'first_name']
class PeriodoAdmin(admin.ModelAdmin):
	list_display=['id', 'per_pe', 'num_exp', 'num_act', 'est_pe']

class ProcedimientoAdmin(admin.ModelAdmin):
	list_display=['des_pro', 'id_mat']
	
class EspecificacionAdmin(admin.ModelAdmin):
	list_display=['id', 'des_esp', 'cos_esp', 'id_pro']

class MateriaAdmin(admin.ModelAdmin):
	list_display=['des_mat']

class PersonaAdmin(admin.ModelAdmin):
	list_display=['id', 'nom_per', 'apepat_per', 'apemat_per', 'numdoc_per']

class ClienteAdmin(admin.ModelAdmin):
	list_display=['id', 'id_per']

class SocioAdmin(admin.ModelAdmin):
	list_display=['id', 'cod_soc', 'id_per']

class ExpedienteAdmin(admin.ModelAdmin):
	list_display=['id', 'num_exp', 'fec_exp', 'tipcon_exp', 'confin_exp']

class SolicitanteAdmin(admin.ModelAdmin):
	list_display=['id', 'id_exp', 'id_per']

class InvitadoAdmin(admin.ModelAdmin):
	list_display=['id', 'id_exp', 'id_per']

class SolicitudAdmin(admin.ModelAdmin):
	list_display=['id', 'fecdoc_sol', 'hecdoc_sol', 'pretsoldoc_sol', 'pretactdoc_sol', 'id_exp']

class ConciliadorAdmin(admin.ModelAdmin):
	list_display=['id', 'fec_doc', 'hor_doc', 'id_exp']

class InvitacionAdmin(admin.ModelAdmin):
	list_display=['id', 'tip_invi', 'fec_invi', 'esc_invi', 'hor_invi']

class AgendaAdmin(admin.ModelAdmin):
	list_display=['id', 'tit_age', 'des_age', 'fecaud_age', 'id_exp']

class InformeAdmin(admin.ModelAdmin):
	list_display=['id', 'tip_inf', 'fec_inf', 'hor_inf', 'id_exp']

class ParcialAdmin(admin.ModelAdmin):
	list_display=['id', 'num_par', 'id_inf']

class ActaAdmin(admin.ModelAdmin):
	list_display=['id', 'num_act', 'id_inf']

class DocumentoAdmin(admin.ModelAdmin):
	list_display=['id', 'tip_doc', 'arcesc_doc', 't_doc', 'id_exp']

class CajaConciliacionAdmin(admin.ModelAdmin):
	list_display=['id', 'ing_con', 'ingcop_con', 'toting_con', 'egre_con', 'id_soc', 'id_exp']

class IngresoConciliacionAdmin(admin.ModelAdmin):
	list_display=['id', 'pacpag_con', 'pagpacade_con', 'desc_con', 'estado_con']

class IngresoConciliacionDetalleAdmin(admin.ModelAdmin):
	list_display=['id', 'monadedet_con', 'fecingdet_con', 'horingdet_con', 'id_cli', 'idpag_con']

class IngresoCopiasAdmin(admin.ModelAdmin):
	list_display=['id', 'monpag_cop', 'cancop_cop', 'fec_cop', 'hor_cop', 'id_cli']

class EgresoDetalleAdmin(admin.ModelAdmin):
	list_display=['id', 'monegre_det', 'tipinv_con', 'fecegredet_con', 'horegredet_con']

admin.site.register(Usuario)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Procedimiento, ProcedimientoAdmin)
admin.site.register(Especificacion, EspecificacionAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Socio, SocioAdmin)
admin.site.register(Expediente, ExpedienteAdmin)
admin.site.register(Solicitante, SolicitanteAdmin)
admin.site.register(Invitado, InvitadoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Conciliador, ConciliadorAdmin)
admin.site.register(Invitacion, InvitacionAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Informe, InformeAdmin)
admin.site.register(Parcial, ParcialAdmin)
admin.site.register(Acta, ActaAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(CajaConciliacion, CajaConciliacionAdmin)
admin.site.register(IngresoConciliacion, IngresoConciliacionAdmin)
admin.site.register(IngresoConciliacionDetalle, IngresoConciliacionDetalleAdmin)
admin.site.register(IngresoCopias, IngresoCopiasAdmin)
admin.site.register(EgresoDetalle, EgresoDetalleAdmin)

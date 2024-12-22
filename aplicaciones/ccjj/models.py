from django.db import models
# Importando
from aplicaciones.ccjj.choices import *
from django.forms import model_to_dict
from datetime import datetime
from siscentroconciliacionjj.settings import STATIC_URL, STATIC_URL, MEDIA_URL

# from django.contrib.auth.models import User
from aplicaciones.user.models import User as Usuario

import locale

locale.setlocale(locale.LC_ALL, 'es_Pe')

# Create your models here.

class Periodo(models.Model):
    per_pe=models.CharField(null=True, blank=True, max_length=4, verbose_name='Año Configuracion')
    num_exp=models.IntegerField(null=True, blank=True, verbose_name='Número de Expediente')
    num_act=models.IntegerField(null=True, blank=True, verbose_name='Número de Acta')
    num_inf=models.IntegerField(null=True, blank=True, verbose_name='Número de Informe')
    est_pe=models.CharField(max_length=10, choices=estado_periodo, default='a', verbose_name='Estado Periodo')

    def __str__(self):
        return self.per_pe

    def toJSON(self):
        item = model_to_dict(self)
        
        return item

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        db_table = 'JJ_PERIODO'
        ordering = ['id']

class Materia(models.Model):
    des_mat = models.CharField(max_length=50, verbose_name='Materia')

    def __str__(self):
        return self.des_mat

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        db_table = 'JJ_MATERIA'
        ordering = ['id']

class Procedimiento(models.Model):
    des_pro = models.CharField(max_length=50, verbose_name='Procedimiento')
    id_mat=models.ForeignKey(Materia, on_delete=models.RESTRICT, verbose_name='Id Materia')

    def __str__(self):
        return self.des_pro

    def toJSON(self):
        item = model_to_dict(self)
        item['mat'] = self.id_mat.toJSON()
        return item

    def toMateria(self):
        return self.id_mat.des_mat

    class Meta:
        verbose_name = 'Procedimiento'
        verbose_name_plural = 'Procedimientos'
        db_table = 'JJ_PROCEDIMIENTO'
        ordering = ['id']

class Especificacion(models.Model):
    des_esp = models.CharField(max_length=100, verbose_name='Especificacion')
    cos_esp = models.FloatField(verbose_name='Costo Conciliacion')
    id_pro=models.ForeignKey(Procedimiento, on_delete=models.RESTRICT, verbose_name='Id Procedimiento')

    def __str__(self):
        return self.des_esp

    def toProcedimiento(self):
        return self.id_pro.toMateria()

    def toJSON(self):
        item = model_to_dict(self)
        item['pro'] = self.id_pro.toJSON()
        return item

    class Meta:
        verbose_name = 'Especificacion'
        verbose_name_plural = 'Especificaciones'
        db_table = 'JJ_ESPECIFICACION'
        ordering = ['id']

class Persona(models.Model):
    nom_per=models.CharField(max_length=255, verbose_name='Nombres')
    apepat_per=models.CharField(max_length=255, verbose_name='Apellido Paterno')
    apemat_per=models.CharField(max_length=255, verbose_name='Apellido Materno')
    numdoc_per=models.CharField(max_length=8, unique=True, verbose_name="DNI")
    eda_per=models.CharField(max_length=2, verbose_name="Edad")
    sex_per=models.CharField(max_length=10, choices=sex_per, default='m', verbose_name='Sexo')
    dir_per=models.CharField(max_length=200, verbose_name='Dirección')
    numcel_per=models.CharField(null=True, blank=True, max_length=9, verbose_name='Número de Celular')  
    ema_per=models.EmailField(null=True, blank=True, max_length=300, verbose_name='Email')

    def __str__(self):
        return '{} {} {}'.format(self.nom_per, self.apepat_per, self.apemat_per)

    def get_full_name(self):
        return '{} | {} {} {}'.format(self.numdoc_per, self.nom_per, self.apepat_per, self.apemat_per)

    def toJSON(self):
        item= model_to_dict(self)
        item['sex_per'] = {'id': self.sex_per, 'name': self.get_sex_per_display()}
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        db_table = 'JJ_PERSONA'
        ordering=['id']

class Cliente(models.Model):
    id_per=models.ForeignKey(Persona, on_delete=models.RESTRICT, verbose_name='Id Persona')
    
    def __str__(self):
        return '{} {} {}'.format(self.id_per.nom_per, self.id_per.apepat_per, self.id_per.apemat_per)
       
    def get_full_name(self):
        return '{} | {} {} {}'.format(self.id_per.numdoc_per, self.id_per.nom_per, self.id_per.apepat_per, self.id_per.apemat_per)
    
    def toJSON(self):
        item= model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['per'] = self.id_per.toJSON()
        return item
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'JJ_CLIENTE'
        ordering=['id']

class Socio(models.Model):
    cod_soc=models.CharField(unique=True, max_length=40, verbose_name='Codigo Socio')
    id_per= models.ForeignKey(Persona, on_delete=models.RESTRICT, verbose_name='Id Persona')

    def __str__(self):
        return '{} {} {}'.format(self.id_per.nom_per, self.id_per.apepat_per, self.id_per.apemat_per)
    
    def toJSON(self):
        item= model_to_dict(self)
        item['per'] = self.id_per.toJSON()
        return item

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        db_table = 'JJ_SOCIO'
        ordering = ['id'] 

class Expediente(models.Model):
    num_exp=models.CharField(max_length=10, verbose_name='Numero de Expediente')
    fec_exp=models.DateField(verbose_name='Fecha Expediente')
    hor_exp=models.TimeField(verbose_name='Hora Expediente')
    proini_exp=models.CharField(max_length=100, null=True, blank=True, verbose_name='Procedimiento Iniciado')
    esttra_exp=models.CharField(max_length=100, null=True, blank=True, verbose_name='Estado Tramite')
    estact_exp=models.CharField(max_length=100, null=True, blank=True, verbose_name='Concluido/No Concluido Con Acta')
    audact_exp=models.CharField(max_length=10, null=True, blank=True, verbose_name='Audicion Unica')
    numfol_exp=models.IntegerField(verbose_name='Numero de Folios')
    confin_exp=models.CharField(max_length=20, null=True, blank=True, verbose_name='Finalizado o No Finalizado')
    inv_exp=models.CharField(max_length=20, null=True, blank=True, verbose_name='Tipo de Invitacion Expediente')
    tipcon_exp=models.CharField(max_length=20, choices=tipoconciliacion_expediente, default='ma', verbose_name='Tipo de Conciliacion')
    id_pe=models.ForeignKey(Periodo, on_delete=models.RESTRICT, verbose_name='Id Periodo', null=True, blank=True)
    id_user=models.ForeignKey(Usuario, on_delete=models.RESTRICT, verbose_name='Id Usuario')
    id_esp= models.ForeignKey(Especificacion, on_delete=models.RESTRICT, verbose_name='Id Especificacion')
    estpro_exp=models.CharField(null=True, max_length=20, choices=estado_proceso, default='exp', verbose_name='Estado de Proceso de Conciliacion')
    
    def __str__(self):
        return self.num_exp

    def get_full_name(self):
        return self.num_exp

    def toJSON(self):
        item= model_to_dict(self)
       
        return item
    
    class Meta:
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'
        db_table = 'JJ_EXPEDIENTE'
        ordering = ['id']

class Solicitante(models.Model):
    id_per= models.ForeignKey(Persona, on_delete=models.RESTRICT, verbose_name='Id Persona')
    id_exp= models.ForeignKey(Expediente, on_delete=models.RESTRICT, verbose_name='Id Expediente')
    
    def __str__(self):
        return self.id_per
    
    class Meta:
        verbose_name = 'Solicitante'
        verbose_name_plural = 'Solicitantes'
        db_table = 'JJ_SOLICITANTE'
        ordering = ['id']

class Invitado(models.Model):
    id_per= models.ForeignKey(Persona, on_delete=models.RESTRICT, verbose_name='id Persona')
    id_exp= models.ForeignKey(Expediente, on_delete=models.RESTRICT, verbose_name='Id Expediente')
    
    def __str__(self):
        return self.id_per
    
    def toJSON(self):
        item= model_to_dict(self)
        item['id_per'] = self.id_per.toJSON()
        return item
    
    class Meta:
        verbose_name = 'Invitado'
        verbose_name_plural = 'Invitados'
        db_table = 'JJ_INVITADO'
        ordering = ['id']

class Solicitud(models.Model):
    fecdoc_sol=models.DateField(null=True, blank=True, verbose_name='Fecha de Solicitud')
    hecdoc_sol=models.CharField(null=True, blank=True, max_length=5000, verbose_name='Hechos de Solicitud')
    pretsoldoc_sol=models.CharField(max_length=5000, verbose_name='Pretension de Solicitud')
    pretactdoc_sol=models.CharField(max_length=5000, verbose_name='Pretension de Acta')
    id_exp= models.ForeignKey(Expediente, on_delete=models.RESTRICT, verbose_name='Id Expediente')

    def __str__(self):
        return self.fecdoc_sol
    
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        db_table = 'JJ_SOLICITUD'
        ordering = ['id']

class Conciliador(models.Model):
    fec_doc=models.DateField(null=True, blank=True, verbose_name='Fecha Documento')
    hor_doc=models.TimeField(null=True, blank=True, verbose_name='Hora Documento')
    id_exp= models.ForeignKey(Expediente, on_delete=models.RESTRICT, verbose_name='Id Expediente')
    
    def __str__(self):
        return self.fec_doc

    class Meta:
        verbose_name = 'Conciliador'
        verbose_name_plural = 'Conciliadores'
        db_table = 'JJ_CONCILIADOR'
        ordering = ['id']  

class Invitacion(models.Model):
    tip_invi=models.CharField(max_length=50, verbose_name='Tipo de Invitacion')
    fec_invi=models.DateField(verbose_name='Fecha de Invitacion')
    hor_invi=models.TimeField(verbose_name='Hora de Invitacion')
    esc_invi=models.FileField(upload_to='Documentos/%Y/%m/%d/', null=True, blank=True, verbose_name='Invitación Escaneado')
    id_inv= models.ForeignKey(Invitado, on_delete=models.RESTRICT, verbose_name='Id Invitado')

    def __str__(self):
        return self.tip_invi

    def get_archivo(self):
        if self.esc_invi:
            return '{}{}'.format(MEDIA_URL, self.esc_invi)
    
    def toJSON(self):
        item= model_to_dict(self)
        item['idexp'] = self.id_inv.id_exp.id
        item['esc_invi'] = self.get_archivo()
        item['idper'] = self.id_inv.id_per.id
        item['nombper'] = self.id_inv.id_per.nom_per + " " + self.id_inv.id_per.apepat_per + " " + self.id_inv.id_per.apemat_per
        
        return item
    
    class Meta:
        verbose_name = 'Invitacion'
        verbose_name_plural = 'Invitaciones'
        db_table = 'JJ_INVITACION'
        ordering = ['id']

class Agenda(models.Model):
    tit_age=models.CharField(max_length=150, verbose_name='Titulo de Agenda')
    des_age=models.CharField(max_length=500, verbose_name='Descripcion de  Agenda')
    tipinvi_age=models.CharField(null=True, max_length=150, verbose_name='Tipo Invitacion')
    fecaud_age=models.DateTimeField(null=True, verbose_name='Fecha de Agenda')
    borcolor_age = models.CharField(null=True, max_length=20, verbose_name="Color Borde")
    foncolor_age = models.CharField(null=True, max_length=20, verbose_name="Color Fondo")
    id_exp= models.ForeignKey(Expediente,on_delete=models.RESTRICT, verbose_name='Id Expediente')
    
    def __str__(self):
        return self.tit_age
    
    class Meta:
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'
        db_table = 'JJ_AGENDA'
        ordering = ['id']

class Informe(models.Model):
    tip_inf=models.CharField(max_length=40, choices=tipoaccta_conciliacion, default='at', verbose_name='Tipo de Informe')
    fec_inf=models.DateField(null=True, blank=True, verbose_name='Fecha Informe')
    hor_inf=models.TimeField(null=True, blank=True, verbose_name='Hora Informe')
    id_exp= models.ForeignKey(Expediente, on_delete=models.RESTRICT, verbose_name='Id Expediente')

    def __str__(self):
        return self.tip_inf

    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'
        db_table = 'JJ_INFORME'
        ordering = ['id']       

class Parcial(models.Model):
    num_par=models.IntegerField(verbose_name='Numero Parcial')
    id_inf= models.ForeignKey(Informe, on_delete=models.RESTRICT, verbose_name='Id Informe')

    def __str__(self):
        return self.num_par

    class Meta:
        verbose_name = 'Parcial'
        verbose_name_plural = 'Parciales'
        db_table = 'JJ_PARCIAL'
        ordering = ['id']  

class Acta(models.Model):
    num_act=models.IntegerField(null=True, blank=True, verbose_name='Numero de Acta')
    id_inf= models.ForeignKey(Informe, on_delete=models.RESTRICT, verbose_name='Id Informe')

    def __str__(self):
        return self.num_act

    """def toJSON(self):
        item= model_to_dict(self)
        item['tipacta_acta'] = {'id': self.tipacta_acta, 'name': self.get_tipacta_acta_display()}
        item['tipinf_acta'] = {'id': self.tipinf_acta, 'name': self.get_tipinf_acta_display()}
        return item"""

    class Meta:
        verbose_name = 'Acta'
        verbose_name_plural = 'Actas'
        db_table = 'JJ_ACTA'
        ordering = ['id']

class Documento(models.Model):
    tip_doc=models.CharField(max_length=100, verbose_name='Titulo de Documento')
    arcesc_doc=models.FileField(upload_to='Documentos/%Y/%m/%d/', null=True, blank=True, verbose_name='Documentos')
    t_doc = models.CharField(null=True, blank=True, max_length=100, verbose_name='Tipo de Documentos')
    id_exp= models.ForeignKey(Expediente, on_delete=models.RESTRICT, verbose_name='Id Expediente')
   
    def __str__(self):
        return self.tip_doc
    
    def get_archivo(self):
        if self.arcesc_doc:
            return '{}{}'.format(MEDIA_URL, self.arcesc_doc)
    
    def toJSON(self):
        item= model_to_dict(self)
        item['arcesc_doc'] = self.get_archivo()
        return item

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        db_table = 'JJ_DOCUMENTO'
        ordering = ['id']  

class CajaConciliacion(models.Model):
    ing_con=models.FloatField(verbose_name='Ingreso Conciliacion')
    ingcop_con=models.FloatField(verbose_name='Ingreso Copias Conciliacion')
    toting_con=models.FloatField(verbose_name='Total Ingreso')
    egre_con=models.FloatField(verbose_name='Egreso')
    id_exp= models.ForeignKey(Expediente, on_delete=models.RESTRICT, verbose_name='id Expediente')
    id_soc= models.ForeignKey(Socio, on_delete=models.RESTRICT, verbose_name='id Socio')
    
    def __str__(self):
        return self.ing_con

    def toJSON(self):
        item= model_to_dict(self)
        item['soc'] = self.id_soc.id_per.toJSON()
        return item

    class Meta:
        verbose_name = 'CajaConciliacion'
        verbose_name_plural = 'CajaConciliaciones'
        db_table = 'JJ_CAJA_CONCILIACION'
        ordering = ['id']

class IngresoConciliacion(models.Model):
    pacpag_con=models.FloatField(verbose_name='Pago Pactado Conciliacion')
    desc_con=models.FloatField(null=True, blank=True, verbose_name='Descuento Conciliacion') 
    pagpacade_con=models.FloatField(verbose_name='Pago Pactado Adelantado Conciliacion')
    estado_con=models.CharField(null=True, blank=True, max_length=50, verbose_name='Estado Ingreso Conciliacion')
    idcaj_con= models.ForeignKey(CajaConciliacion, on_delete=models.RESTRICT, verbose_name='id Persona')
    
    def __str__(self):
        return self.pacpag_con

    def toJSON(self):
        item= model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'IngresoConciliacion'
        verbose_name_plural = 'IngresosConciliaciones'
        db_table = 'JJ_INGRESO_CONCILIACION'
        ordering = ['id']

class IngresoConciliacionDetalle(models.Model):
    monadedet_con=models.FloatField(verbose_name='Monto Adelantado Detalle Conciliacion')
    fecingdet_con=models.DateField(null=True, blank=True, verbose_name='Fecha Ingreso Conciliacion Detalle')
    horingdet_con=models.TimeField(null=True, blank=True, verbose_name='Hora Ingreso Conciliacion Detalle')
    idpag_con= models.ForeignKey(IngresoConciliacion, on_delete=models.RESTRICT, verbose_name='id Ingreso Conciliacion')
    id_cli= models.ForeignKey(Persona, on_delete=models.RESTRICT, verbose_name='id Cliente')
    
    def __str__(self):
        return self.monadedet_con

    def toJSON(self):
        item= model_to_dict(self)
        item['cliente'] = self.id_cli.toJSON()
        return item

    class Meta:
        verbose_name = 'IngresoConciliacionDetalle'
        verbose_name_plural = 'IngresoConciliacionDetalles'
        db_table = 'JJ_INGRESO_CONCILIACION_DETALLE'
        ordering = ['id']

class IngresoCopias(models.Model):
    monpag_cop=models.FloatField(verbose_name='Monto Pago Copias')
    cancop_cop=models.IntegerField(null=True, blank=True, verbose_name='Cantidad Copias')
    fec_cop=models.DateField(null=True, blank=True, verbose_name='Fecha Copias')
    hor_cop=models.TimeField(null=True, blank=True, verbose_name='Hora Copias')
    id_cli= models.ForeignKey(Persona, on_delete=models.RESTRICT, verbose_name='id Cliente', null=True, blank=True)
    idcaj_con= models.ForeignKey(CajaConciliacion, on_delete=models.RESTRICT, verbose_name='id Caja Conciliacion')
   
    def __str__(self):
        return self.monpag_cop

    def toJSON(self):
        item= model_to_dict(self)
        item['cliente'] = self.id_cli.toJSON()
        return item

    class Meta:
        verbose_name = 'IngresoCopia'
        verbose_name_plural = 'IngresoCopias'
        db_table = 'JJ_INGRESO_COPIAS'
        ordering = ['id']

class EgresoDetalle(models.Model):
    monegre_det=models.FloatField(verbose_name='Monto Egreso')
    fecegredet_con=models.DateField(null=True, blank=True, verbose_name='Fecha Egreso Conciliacion Detalle')
    horegredet_con=models.TimeField(null=True, blank=True, verbose_name='Hora Egreso Conciliacion Detalle')
    tipinv_con=models.CharField(max_length=50, verbose_name='Tipo Invitacion Conciliacion')
    idcaj_con= models.ForeignKey(CajaConciliacion, on_delete=models.RESTRICT, verbose_name='id Caja Conciliacion')
    def __str__(self):
        return self. monegre_det

    def toJSON(self):
        item= model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'EgresoDetalle'
        verbose_name_plural = 'EgresoDetalles'
        db_table = 'JJ_EGRESO_DETALLE'
        ordering = ['id']

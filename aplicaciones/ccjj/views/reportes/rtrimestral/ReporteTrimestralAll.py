
from aplicaciones.ccjj.models import Expediente, Informe, Procedimiento, Acta, Solicitud

from datetime import datetime, timedelta

class ReporteTrimestralAll():

    # Para saber Procedimientos Iniciados de Materia
    def datosProcedimientosIniciados(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Expediente.objects.filter(id_esp__id_pro=idpro, fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber En Tramite de Materia 
    def datosEnTramite(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Expediente.objects.exclude(esttra_exp='').filter(id_esp__id_pro=idpro, fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Concluido Acuerdo Total (cat) de Materia 
    def datosConcluidoAcuerdoTotal(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='at', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Concluido Acuerdo Parcial (cap) de Materia 
    def datosConcluidoAcuerdoParcial(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ap', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
        
    # Para saber Concluido Falta de Acuerdo (cfa) de Materia 
    def datosConcluidoFaltaAcuerdo(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='fa', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Concluido Inasistencia Solicitante (ciups) de Materia 
    def datosConcluidoInasistenciaSolicitante(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='is', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Concluido Inasistencia Invitado (ciupi) de Materia 
    def datosConcluidoInasistenciaInvitado(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ii', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Concluido Inasistencia Ambas Partes (ciap) de Materia 
    def datosConcluidoInasistenciaAmbasPartes(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='iap', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Concluido Acta Motivida (cdmc) de Materia 
    def datosConcluidoDesicionMotivaConciliador(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='am', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Concluido Con Informe (cci) de Materia 
    def datosConcluidoInforme(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ci', id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluidos (tc) de Materia 
    def datosTotalConcluidos(self, idpro, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(id_exp__id_esp__id_pro=idpro, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # ##############################################################    
    # Para Saber la Totalidad de Procedimientos Iniciados de Materias
    def datosTotalProcedimientosIniciados(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Expediente.objects.filter(id_esp__id_pro__id_mat__id=idmat, fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para Saber la Totalidad de Estado En Tramite de Materias
    def datosTotalEstadoTramite(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Expediente.objects.exclude(esttra_exp='').filter(id_esp__id_pro__id_mat__id=idmat, fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluido Acuerdo Total (cat) de Materias
    def datosTotalConcluidoAcuerdoTotal(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='at', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluido Acuerdo Parcial (cap) de Materias
    def datosTotalConcluidoAcuerdoParcial(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ap', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Toal Concluido Falta de Acuerdo (cfa) de Materias
    def datosTotalConcluidoFaltaAcuerdo(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='fa', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluido Inasistencia Solicitante (ciups) de Materias
    def datosTotalConcluidoInasistenciaSolicitante(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='is', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluido Inasistencia Invitado (ciupi) de Materias
    def datosTotalConcluidoInasistenciaInvitado(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ii', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluido Inasistencia Ambas Partes (ciap) de Materias
    def datosTotalConcluidoInasistenciaAmbasPartes(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='iap', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluido Acta Motivida (cdmc) de Materias
    def datosTotalConcluidoDesicionMotivaConciliador(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='am', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total Concluido Con Informe (cci) de Materias
    def datosTotalConcluidoInforme(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ci', id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Total Concluidos (tc) de Materias Total
    def datosTotalConcluidosTotal(self, idmat, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(id_exp__id_esp__id_pro__id_mat__id=idmat, id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # ###############################################################

    # Para Saber la Total General de Procedimientos Iniciados de Materias
    def datosTotalGeneralProcedimientosIniciados(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Expediente.objects.filter(fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para Saber la Total General de Estado En Tramite de Materias
    def datosTotalGeneralEstadoTramite(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Expediente.objects.exclude(esttra_exp='').filter(fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Acuerdo Total (cat) de Materias
    def datosTotalGeneralConcluidoAcuerdoTotal(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='at', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Acuerdo Parcial (cap) de Materias
    def datosTotalGeneralConcluidoAcuerdoParcial(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ap', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Falta de Acuerdo (cfa) de Materias
    def datosTotalGeneralConcluidoFaltaAcuerdo(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='fa', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Inasistencia Solicitante (ciups) de Materias
    def datosTotalGeneralConcluidoInasistenciaSolicitante(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='is', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Inasistencia Invitado (ciupi) de Materias
    def datosTotalGeneralConcluidoInasistenciaInvitado(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ii', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Inasistencia Ambas Partes (ciap) de Materias
    def datosTotalGeneralConcluidoInasistenciaAmbasPartes(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='iap', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Acta Motivida (cdmc) de Materias
    def datosTotalGeneralConcluidoDesicionMotivaConciliador(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='am', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
    
    # Para saber Total General Concluido Con Informe (cci) de Materias
    def datosTotalGeneralConcluidoInforme(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(tip_inf='ci', id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp

    # Para saber Total General Concluidos (tc) de Materias Total
    def datosTotalGeneralConcluidosTotal(self, fechdesde, fechhasta):
        datoresp=0
        datoresp=Informe.objects.filter(id_exp__fec_exp__range=(fechdesde,fechhasta)).count()
        return datoresp
# IMPORTANDO MODELOS
from aplicaciones.ccjj.models import Periodo, Expediente

from datetime import datetime

class ExpedienteDatos:
    def numexp(self):
        for i in Periodo.objects.filter(est_pe='a'):
            return i.num_exp
    
    def fecha(self):
        fechaactual=datetime.now()
        for i in Periodo.objects.filter(est_pe='a'):
            fechaexp=i.per_pe
        return fechaexp + '-' + fechaactual.strftime("%m-%d")
    
    def hora(self):
        horaactual=datetime.now()
        return horaactual.strftime('%H:%M:%S')
    
    def year(self):
        for i in Periodo.objects.filter(est_pe='a'):
            return i.per_pe
        
    def numexpYear(self, idexp):
        for i in Expediente.objects.filter(id=idexp):
            return str(i.num_exp) + ' - ' + str(i.fec_exp.strftime("%Y"))

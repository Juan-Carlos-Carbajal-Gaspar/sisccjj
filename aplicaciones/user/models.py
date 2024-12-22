from django.db import models

from aplicaciones.user.choices import *

from django.contrib.auth.models import AbstractUser

from crum import get_current_request
from django.forms import model_to_dict

from siscentroconciliacionjj.settings import STATIC_URL, STATIC_URL, MEDIA_URL

# Create your models here.

class User(AbstractUser):
    img_user=models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True, verbose_name='Avatar')
    tke_user = models.UUIDField(primary_key=False, editable=False, null=True, blank=True, verbose_name='Token')
    dni_user=models.CharField(max_length=8, unique=True, verbose_name="DNI")
    esp_user=models.CharField(max_length=50, null=True, blank=True, verbose_name='Especialidad')
    rgf_user = models.CharField(max_length=20, null=True, blank=True, verbose_name='Registro de Familia')
    rgg_user = models.CharField(max_length=20, null=True, blank=True, verbose_name='Registro General')
    gen_user=models.CharField(max_length=10, choices=genero_usuarios, default='m', verbose_name='Genero')

    def get_image(self):
        if self.img_user:
            return '{}{}'.format(MEDIA_URL, self.img_user)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['img_user'] = self.get_image()
        item['gen_user'] = {'id': self.gen_user, 'name': self.get_gen_user_display()}
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
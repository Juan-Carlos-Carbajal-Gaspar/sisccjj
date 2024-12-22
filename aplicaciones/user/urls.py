from django.urls import path
from aplicaciones.user.views import *

app_name = 'user'

urlpatterns = [
    # user
    path('listarusuario/', ListarUsuarioView.as_view(), name='user_listarusuario'),
    path('crearusuario/', CrearUsuarioView.as_view(), name='user_crearusuario'),
    path('editarusuario/<int:pk>/', EditarUsuarioView.as_view(), name='user_editarusuario'),
    # # path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('change/group/<int:pk>/', UserChangeGroup.as_view(), name='user_change_group'),
    path('editarperfilusuario/', EditarPerfilUserView.as_view(), name='user_editarperfilusuario'),
    path('cambiarcontraseña/', CambiarContrasenaView.as_view(), name='user_editarcontrasena'),
]

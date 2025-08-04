from django.urls import path
from django.views.generic import TemplateView
from django.http import JsonResponse

from . import views

# Ruta auxiliar para eliminación de datos desde Facebook
def eliminar_datos_facebook(request):
    return JsonResponse({
        "mensaje": "Si deseas eliminar tus datos, por favor contáctanos a projobsadmin2025@gmail.com."
    })

urlpatterns = [
    # Página de inicio
    path('', views.index, name='index'),

    # Autenticación
    path('inicioSesion/', views.inicioSesion, name='inicioSesion'),
    path('formulario/', views.formulario, name='formulario'),

    # Usuario
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('perfilusuario/', views.perfilusuario, name='perfilusuario'),          # Vista del perfil del usuario logueado
    path('perfiltrabajador/', views.perfiltrabajador, name='perfiltrabajador'),  # Vista específica del trabajador logueado
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('trabajadores/', views.ver_trabajadores, name='ver_trabajadores'),      # Búsqueda y listado de trabajadores

    # Ofertas y postulaciones
    path('crear-oferta/', views.crear_oferta, name='crear_oferta'),              # Crear una nueva oferta laboral
    path('lista_ofertas/', views.lista_ofertas, name='lista_ofertas'),          # Listado de ofertas activas
    path('marcar_revisada/', views.marcar_como_revisada, name='marcar_revisada'), # Marcar postulaciones como revisadas
    path('historial/', views.historial_postulaciones, name='historial_postulaciones'), # Historial del usuario
    path('contratos/', views.contratos_usuario, name='contratos_usuario'),      # Vista de contratos desde la perspectiva del cliente
    path('finalizar_postulacion/<int:id>/', views.finalizar_postulacion, name='finalizar_postulacion'), # Finalizar contrato
    path('mis-contratos/', views.contratos_trabajador, name='contratos_trabajador'),    # Vista de contratos desde la perspectiva del trabajador

    # Chat
    path('chat/<int:id_usuario>/', views.chat_con_usuario, name='chat_con_usuario'),

    # Notificaciones
    path('notificaciones/', views.obtener_notificaciones, name='obtener_notificaciones'),
    path('notificaciones/marcar/', views.marcar_notificaciones_leidas, name='marcar_notificaciones_leidas'),

    # Perfil de otro trabajador
    path('trabajador/<int:id>/', views.perfil_trabajador_detalle, name='perfil_trabajador_detalle'),

    # Subida de evidencias
    path('subir_evidencia/', views.subir_evidencia_view, name='subir_evidencia'),

    # Panel administrativo personalizado
    path('admin-usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard-graficos/', views.admin_dashboard_graficos, name='admin_dashboard_graficos'),
    path('admin-ofertas/', views.admin_ofertas, name='admin_ofertas'),
    path('admin-postulaciones/', views.admin_postulaciones, name='admin_postulaciones'),
    path('admin-calificaciones/', views.admin_calificaciones, name='admin_calificaciones'),
    path('admin-calificaciones/eliminar/<int:id>/', views.admin_eliminar_calificacion, name='admin_eliminar_calificacion'),
    path('admin-evidencias/', views.admin_evidencias, name='admin_evidencias'),
    path('admin-evidencias/eliminar/<int:id>/', views.admin_eliminar_evidencia, name='admin_eliminar_evidencia'),
    path('admin-chats/', views.admin_chats, name='admin_chats'),
    path('admin-chats/<int:usuario1_id>/<int:usuario2_id>/', views.admin_ver_chat, name='admin_ver_chat'),

    # Políticas de privacidad
    path('privacidad/', TemplateView.as_view(template_name='politica_privacidad.html'), name='privacidad'),
    path('eliminar-datos/', TemplateView.as_view(template_name='eliminar_datos.html'), name='eliminar_datos'),
]

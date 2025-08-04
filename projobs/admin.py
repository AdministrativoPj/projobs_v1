# Importación del módulo de administración de Django
from django.contrib import admin

# Importación de los modelos que se van a registrar en el admin
from .models import Usuario, OfertaLaboralIndependiente, MensajeContacto

# Registro del modelo Usuario en el panel de administración
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Campos que se mostrarán como columnas en la tabla del admin
    list_display = ('nombre', 'apellido', 'correo', 'rol')

    # Campos por los que se puede buscar desde el buscador del admin
    search_fields = ('nombre', 'apellido', 'correo')

    # Filtros laterales para segmentar por rol
    list_filter = ('rol',)


# Registro del modelo OfertaLaboralIndependiente en el admin
@admin.register(OfertaLaboralIndependiente)
class OfertaLaboralIndependienteAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista de ofertas
    list_display = ('titulo', 'cliente', 'modo_trabajo', 'categoria', 'fecha_limite', 'estado')

    # Búsqueda por título, descripción o nombre del cliente (relación foránea)
    search_fields = ('titulo', 'descripcion', 'cliente__nombre')

    # Filtros para modo de trabajo, categoría y estado de la oferta
    list_filter = ('modo_trabajo', 'categoria', 'estado')

    # Barra de navegación por fechas usando el campo 'fecha_publicacion'
    date_hierarchy = 'fecha_publicacion'


# Registro del modelo MensajeContacto en el panel de administración
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    # Muestra nombre, correo y contenido del mensaje en la tabla
    list_display = ('nombre', 'correo', 'mensaje')

    # Permite buscar por nombre y correo del remitente
    search_fields = ('nombre', 'correo')

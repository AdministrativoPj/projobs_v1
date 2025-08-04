# Importa la clase base AppConfig desde Django, usada para configurar la app
from django.apps import AppConfig

# Definición de la configuración de la aplicación "projobs"
class ProjobsConfig(AppConfig):
    # Especifica el tipo de campo automático que se usará por defecto para las claves primarias
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación. Debe coincidir con el nombre del directorio donde está la app
    name = 'projobs'

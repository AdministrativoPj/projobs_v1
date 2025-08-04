# projobs/pipeline.py
from projobs.models import Usuario

# Esta función se ejecuta como parte del flujo de autenticación social (Google o Facebook)
def create_usuario_record(backend, user, response, *args, **kwargs):
    email = ''
    first_name = ''
    last_name = ''

    try:
        # Si el backend es Facebook, extraemos los datos del objeto response de Facebook
        if backend.name == 'facebook':
            email = response.get('email', '')  # Email proporcionado por Facebook
            first_name = response.get('first_name', '')  # Primer nombre
            last_name = response.get('last_name', '')  # Apellido

            # Si no hay nombres separados, se intenta dividir el campo 'name'
            if not first_name and not last_name and 'name' in response:
                parts = response['name'].split(' ', 1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''

        # Si el backend es Google, tomamos los datos respectivos
        elif backend.name == 'google-oauth2':
            email = response.get('email', '')  # Email de Google
            first_name = response.get('given_name', '')  # Nombre
            last_name = response.get('family_name', '')  # Apellido

        # Si el correo no existe en la base de datos, se crea el usuario
        if email and not Usuario.objects.filter(correo=email).exists():
            Usuario.objects.create(
                nombre=first_name or 'Usuario',  # Si no hay nombre, se usa 'Usuario' como fallback
                apellido=last_name or '',  # Apellido vacío si no hay dato
                correo=email,  # Email del proveedor OAuth
                password='',  # Sin contraseña (se supone autenticación social)
                rol=2  # Rol por defecto: Cliente
            )

    except Exception as e:
        # En caso de error, se registra en el log para depuración
        import logging
        logging.exception("Error en pipeline create_usuario_record")
        raise e  # Se relanza la excepción para visibilidad en desarrollo

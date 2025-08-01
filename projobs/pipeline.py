# projobs/pipeline.py
from projobs.models import Usuario

def create_usuario_record(backend, user, response, *args, **kwargs):
    email = ''
    first_name = ''
    last_name = ''

    try:
        if backend.name == 'facebook':
            email = response.get('email', '')
            first_name = response.get('first_name', '')
            last_name = response.get('last_name', '')
            if not first_name and not last_name and 'name' in response:
                parts = response['name'].split(' ', 1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''
        elif backend.name == 'google-oauth2':
            email = response.get('email', '')
            first_name = response.get('given_name', '')
            last_name = response.get('family_name', '')

        if email and not Usuario.objects.filter(correo=email).exists():
            Usuario.objects.create(
                nombre=first_name or 'Usuario',
                apellido=last_name or '',
                correo=email,
                password='',
                rol=2
            )
    except Exception as e:
        import logging
        logging.exception("Error en pipeline create_usuario_record")
        raise e  # Para ver el error completo en los logs

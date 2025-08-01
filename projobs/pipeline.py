from projobs.models import Usuario
from django.contrib.auth.models import User

def create_usuario_record(backend, user, response, *args, **kwargs):
    email = ''
    first_name = ''
    last_name = ''

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

    # Crea usuario de tu modelo personalizado si no existe
    if email and not Usuario.objects.filter(correo=email).exists():
        Usuario.objects.create(
            nombre=first_name or '',
            apellido=last_name or '',
            correo=email,
            password='',  # sin password porque usa social login
            rol=2
        )

    # También crea un usuario Django si no existe
    if email and not User.objects.filter(username=email).exists():
        User.objects.create_user(
            username=email,
            email=email,
            password=None,  # sin password
            first_name=first_name,
            last_name=last_name
        )

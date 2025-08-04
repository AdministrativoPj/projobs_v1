# Importación de módulos necesarios para definir modelos
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# -------------------------
# Modelo personalizado de Usuario
# -------------------------
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del usuario
    apellido = models.CharField(max_length=100)  # Apellido del usuario
    correo = models.EmailField(unique=True)  # Correo electrónico único
    password = models.CharField(max_length=254)  # Contraseña en texto plano (⚠️ deberías cifrarla)

    # Opciones de roles posibles para el usuario
    ROLES = (
        (1, "Admin"),
        (2, "Cliente"),
        (3, "Trabajador"),
    )
    rol = models.IntegerField(choices=ROLES, default=2)  # Rol asignado al usuario
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)  # Foto de perfil
    token_recuperacion = models.CharField(max_length=255, null=True, blank=True)  # Token temporal para recuperación de contraseña

    def promedio_calificaciones(self):
        # Calcula el promedio de calificaciones recibidas como trabajador
        promedio = self.calificaciones_recibidas.aggregate(avg=Avg('puntuacion'))['avg']
        return round(promedio, 1) if promedio else None

    def __str__(self):
        # Representación legible del usuario
        return f"{self.nombre} {self.apellido} - {self.correo}"

# -------------------------
# Modelo de Oferta Laboral publicada por un cliente
# -------------------------
class OfertaLaboralIndependiente(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Cliente que crea la oferta
    titulo = models.CharField(max_length=100)  # Título de la oferta
    descripcion = models.TextField()  # Descripción detallada del trabajo
    ubicacion = models.CharField(max_length=100)  # Ubicación geográfica del trabajo

    # Tipos de modalidad de trabajo
    MODO_TRABAJO = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido')
    ]
    modo_trabajo = models.CharField(max_length=20, choices=MODO_TRABAJO)

    rango_pago = models.CharField(max_length=50)  # Valor estimado del pago
    fecha_limite = models.DateField()  # Fecha máxima para aplicar a la oferta
    max_postulaciones = models.PositiveIntegerField(default=5)  # Máximo de trabajadores que se pueden postular

    # Categorías de profesión
    PROFESIONES = [
        ('Electricista', 'Electricista'),
        ('Diseñador Gráfico', 'Diseñador Gráfico'),
        ('Programador', 'Programador'),
        ('Plomero', 'Plomero'),
        ('Jardinero', 'Jardinero'),
        ('Otro', 'Otro'),
    ]
    categoria = models.CharField(max_length=50, choices=PROFESIONES)
    descripcion_profesion = models.CharField(max_length=100, blank=True)  # Si la categoría es "Otro"

    estado = models.CharField(max_length=20, default='abierta')  # Estado de la oferta (abierta/cerrada)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)  # Fecha de publicación automática

    def __str__(self):
        return self.titulo  # Representación legible de la oferta

# -------------------------
# Modelo de mensajes desde el formulario de contacto
# -------------------------
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del remitente
    correo = models.EmailField()  # Correo de quien escribe
    mensaje = models.TextField()  # Contenido del mensaje
    fecha_envio = models.DateTimeField(auto_now_add=True)  # Fecha en que fue enviado

    def __str__(self):
        return f"{self.nombre} ({self.correo}) - {self.fecha_envio.strftime('%Y-%m-%d %H:%M')}"

# -------------------------
# Modelo que vincula trabajadores con ofertas: la postulación
# -------------------------
class Postulacion(models.Model):
    # Estados posibles de la postulación
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    trabajador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='postulaciones')  # Usuario que se postula
    oferta = models.ForeignKey(OfertaLaboralIndependiente, on_delete=models.CASCADE, related_name='postulaciones')  # Oferta asociada
    fecha_postulacion = models.DateTimeField(auto_now_add=True)  # Fecha de postulación
    revisada = models.BooleanField(default=False)  # Si ya fue revisada por el cliente
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')  # Estado actual
    finalizada = models.BooleanField(default=False)  # Si el trabajo fue completado

    class Meta:
        unique_together = ('trabajador', 'oferta')  # Evita postulaciones duplicadas a la misma oferta

    def __str__(self):
        return f"{self.trabajador.nombre} -> {self.oferta.titulo} [{self.estado}]"

# -------------------------
# Modelo de chat entre usuarios (emisor y receptor)
# -------------------------
class Mensaje(models.Model):
    emisor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='mensajes_enviados')  # Usuario que envía el mensaje
    receptor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='mensajes_recibidos')  # Usuario que lo recibe
    contenido = models.TextField()  # Texto del mensaje
    fecha_envio = models.DateTimeField(auto_now_add=True)  # Fecha de envío
    leido = models.BooleanField(default=False)  # Estado de lectura

    def __str__(self):
        return f"{self.emisor} ➜ {self.receptor} : {self.contenido[:30]}"

# -------------------------
# Modelo de calificaciones entre cliente y trabajador
# -------------------------
class Calificacion(models.Model):
    trabajador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="calificaciones_recibidas")  # Quien recibe la calificación
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="calificaciones_realizadas")  # Quien califica
    puntuacion = models.IntegerField()  # Valor entre 1 y 5
    comentario = models.TextField()  # Opinión
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trabajador', 'cliente')  # Solo una calificación por cliente-trabajador

    def __str__(self):
        return f"{self.cliente} → {self.trabajador}: {self.puntuacion}"

# -------------------------
# Evidencias que puede subir un trabajador sobre su trabajo
# -------------------------
class Evidencia(models.Model):
    trabajador = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 3})  # Solo trabajadores
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE)  # A qué postulación pertenece
    archivo = models.FileField(upload_to='evidencias/')  # Archivo subido (imagen, PDF, etc.)
    descripcion = models.TextField(blank=True)  # Descripción opcional
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidencia de {self.trabajador.nombre} - {self.fecha.strftime('%Y-%m-%d')}"

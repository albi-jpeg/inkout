from django.db import models
from django.utils.timezone import now
from usuarios.models import MyUser

#Modelo artistas
class Artista(models.Model):
    usuario = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='artista', null=True, blank=True) 
    nombre_artistico = models.CharField(max_length=100, verbose_name='Nombre_Artistico', blank=True)
    foto_perfil = models.ImageField(verbose_name='Foto_perfil', null=True, blank=True)
    biografia = models.TextField(max_length=500, verbose_name='Biografia', blank=True)
    sitio_web = models.URLField(blank=True)

    def __str__(self):
        return self.nombre_artistico

#Modelo promociones
class Promocion(models.Model):
    titulo = models.CharField(max_length=100, verbose_name= 'Titulo')
    descripcion = models.TextField(max_length=500, verbose_name= 'Descripcion')
    fecha_fin = models.DateField()
    codigo_qr = models.ImageField(verbose_name = 'QR', null=True)

    def __str__(self):
        return self.titulo

#Modelo diseños
class Disenyo(models.Model):
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, related_name='disenos')
    titulo = models.CharField(max_length=100, verbose_name= 'Titulo')
    descripcion = models.TextField(max_length=500, verbose_name= 'Descripcion')
    imagen = models.ImageField(verbose_name = 'Imagen', null=True, blank=True)

    def __str__(self):
        return self.titulo
 
#Modelo citas    
class Cita(models.Model):
    #Definimos manualmente tres tipos de estado de las citas
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('vencida', 'Vencida')
    )

    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, related_name='citas')
    usuario = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='usuario')
    mensaje = models.TextField(null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    
    class Meta:
        constraints = [
            # Un usuario no puede tener dos citas el mismo día
            models.UniqueConstraint(fields=['usuario', 'fecha'], name='unique_usuario_fecha'),

            # Un artista no puede tener dos citas a la misma fecha y hora
            models.UniqueConstraint(fields=['artista', 'fecha', 'hora'], name='unique_artista_fecha_hora'),
        ]

    def __str__(self):
        return self.fecha.strftime('%d/%m/%Y')
 
#Modelo mensajes
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - {self.asunto}'

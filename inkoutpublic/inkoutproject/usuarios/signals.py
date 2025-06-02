from django.db.models.signals import post_save
from django.dispatch import receiver
from inkoutapp.models import Artista
from usuarios.models import MyUser  # asegúrate de importar correctamente MyUser

@receiver(post_save, sender=MyUser)
def create_artista(sender, instance, created, **kwargs):
    if created and instance.user_type == 'artista':
        Artista.objects.create(usuario=instance)  

from django.contrib import admin
from django.contrib import admin
from .models import Artista, Promocion, Disenyo, Cita, MensajeContacto

class ArtistaAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('usuario','nombre_artistico')

class PromocionAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('titulo', 'codigo_qr')

class DisenyoAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('artista', 'titulo')

class CitaAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('artista', 'usuario', 'fecha', 'hora')

class MensajeAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('nombre', 'telefono', 'asunto', 'mensaje', 'fecha')


admin.site.register(Artista, ArtistaAdmin)
admin.site.register(Promocion, PromocionAdmin)
admin.site.register(Disenyo, DisenyoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(MensajeContacto, MensajeAdmin)


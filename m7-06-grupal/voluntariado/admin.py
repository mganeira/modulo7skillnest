from django.contrib import admin
from .models import Voluntario, Evento


@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    """Configuración del admin para Voluntarios"""
    list_display = ('nombre', 'email', 'telefono', 'fecha_registro', 'eventos_asignados')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha_registro',)
    readonly_fields = ('fecha_registro',)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Configuración del admin para Eventos"""
    list_display = ('titulo', 'fecha', 'cantidad_voluntarios')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('fecha',)
    filter_horizontal = ('voluntarios',)

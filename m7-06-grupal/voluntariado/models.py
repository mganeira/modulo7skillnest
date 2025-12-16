from django.db import models


class Voluntario(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    def eventos_asignados(self):
        """Método para mostrar cantidad de eventos en el admin"""
        return self.eventos.count()
    eventos_asignados.short_description = 'Eventos'

    class Meta:
        verbose_name = 'Voluntario'
        verbose_name_plural = 'Voluntarios'


class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateField()
    voluntarios = models.ManyToManyField(Voluntario, related_name="eventos", blank=True)

    def __str__(self):
        return self.titulo
    
    def cantidad_voluntarios(self):
        """Método para mostrar cantidad de voluntarios en el admin"""
        return self.voluntarios.count()
    cantidad_voluntarios.short_description = 'Voluntarios'

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha']
from django.db import models

# 2.1. Relación Muchos a Uno (ForeignKey)
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')
    estudiantes = models.ManyToManyField('Estudiante', through='Inscripcion')

    def __str__(self):
        return self.nombre

# 2.2. Relación Muchos a Muchos (ManyToManyField) con Entidad Intermedia
class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Inscripcion(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('F', 'Finalizado'),
    ]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    nota_final = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('estudiante', 'curso')

    def __str__(self):
        return f'{self.estudiante.nombre} en {self.curso.nombre}'

# 2.3. Relación Uno a Uno (OneToOneField)
class Perfil(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, primary_key=True)
    biografia = models.TextField(blank=True)
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    redes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Perfil de {self.estudiante.nombre}'


from django.contrib import admin
from .models import Profesor, Curso, Estudiante, Perfil, Inscripcion

# Opciones de visualización para Inscripcion en el admin de Curso y Estudiante
class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 1 # Cuántos formularios de inscripción extra mostrar

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')
    search_fields = ('nombre', 'email')

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor')
    list_filter = ('profesor',)
    search_fields = ('nombre', 'descripcion')
    inlines = [InscripcionInline] # Permite ver/añadir inscripciones desde la página del curso

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')
    search_fields = ('nombre', 'email')
    inlines = [InscripcionInline] # Permite ver/añadir inscripciones desde la página del estudiante

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'biografia')
    search_fields = ('estudiante__nombre',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'fecha_inscripcion', 'estado', 'nota_final')
    list_filter = ('estado', 'curso')
    search_fields = ('estudiante__nombre', 'curso__nombre')


from django.shortcuts import render
from .models import Profesor, Curso, Estudiante, Perfil, Inscripcion
from django.views.generic import ListView, DetailView


def welcome_view(request):
    return render(request, 'academico/base.html')

class ProfesorListView(ListView):
    model = Profesor
    template_name = 'academico/profesor_list.html'
    context_object_name = 'profesores'

class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = 'academico/profesor_detail.html'
    context_object_name = 'profesor'

class CursoListView(ListView):
    model = Curso
    template_name = 'academico/curso_list.html'
    context_object_name = 'cursos'

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'academico/curso_detail.html'
    context_object_name = 'curso'

class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'academico/estudiante_list.html'
    context_object_name = 'estudiantes'

class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'academico/estudiante_detail.html'
    context_object_name = 'estudiante'


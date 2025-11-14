from django.urls import path
from .views import (
    ProfesorListView, ProfesorDetailView,
    CursoListView, CursoDetailView,
    EstudianteListView, EstudianteDetailView,
    welcome_view
)

app_name = 'academico'
urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('profesores/', ProfesorListView.as_view(), name='profesor_list'),
    path('profesores/<int:pk>/', ProfesorDetailView.as_view(), name='profesor_detail'),
    path('cursos/', CursoListView.as_view(), name='curso_list'),
    path('cursos/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('estudiantes/', EstudianteListView.as_view(), name='estudiante_list'),
    path('estudiantes/<int:pk>/', EstudianteDetailView.as_view(), name='estudiante_detail'),
]

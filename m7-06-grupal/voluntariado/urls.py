from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voluntarios/', views.voluntario_list, name='voluntario_list'),
    path('eventos/', views.evento_list, name='evento_list'),
    path('voluntarios/crear/', views.voluntario_create, name='voluntario_create'),
    path('eventos/crear/', views.evento_create, name='evento_create'),
    path('voluntarios/editar/<int:id>/', views.voluntario_update, name='voluntario_update'),
    path('eventos/editar/<int:id>/', views.evento_update, name='evento_update'),
    path('voluntarios/eliminar/<int:id>/', views.voluntario_delete, name='voluntario_delete'),
    path('eventos/eliminar/<int:id>/', views.evento_delete, name='evento_delete'),
    path('voluntarios/detalle/<int:id>/', views.voluntario_detail, name='voluntario_detail'),
    path('eventos/detalle/<int:id>/', views.evento_detail, name='evento_detail'),
]
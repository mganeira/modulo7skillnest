from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Voluntario, Evento
from .forms import VoluntarioForm, EventoForm


# ============ VISTAS PRINCIPALES ============

def home(request):
    """Vista principal de la aplicación"""
    total_voluntarios = Voluntario.objects.count()
    total_eventos = Evento.objects.count()
    
    context = {
        'total_voluntarios': total_voluntarios,
        'total_eventos': total_eventos,
    }
    return render(request, 'home.html', context)


# ============ VISTAS DE VOLUNTARIOS ============

def voluntario_list(request):
    """Ejercicio 6: Listado de todos los voluntarios"""
    voluntarios = Voluntario.objects.all().order_by('-fecha_registro')
    return render(request, 'voluntario_list.html', {'voluntarios': voluntarios})

def voluntario_detail(request, id):
    """Vista detallada de un voluntario con sus eventos"""
    voluntario = get_object_or_404(Voluntario, id=id)
    eventos = voluntario.eventos.all()
    
    return render(request, 'voluntario_detail.html', {
        'voluntario': voluntario,
        'eventos': eventos
    })

def voluntario_create(request):
    """Ejercicio 7: Crear un nuevo voluntario"""
    if request.method == 'POST':
        form = VoluntarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Voluntario creado exitosamente.')
            return redirect('voluntario_list')
    else:
        form = VoluntarioForm()
    
    return render(request, 'voluntario_form.html', {
        'form': form,
        'titulo': 'Nuevo Voluntario',
        'boton': 'Crear Voluntario'
    })


def voluntario_update(request, id):
    """Ejercicio 8: Modificar un voluntario existente"""
    voluntario = get_object_or_404(Voluntario, id=id)
    
    if request.method == 'POST':
        form = VoluntarioForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Voluntario "{voluntario.nombre}" actualizado exitosamente.')
            return redirect('voluntario_list')
    else:
        form = VoluntarioForm(instance=voluntario)
    
    return render(request, 'voluntario_form.html', {
        'form': form,
        'titulo': f'Editar Voluntario: {voluntario.nombre}',
        'boton': 'Actualizar Voluntario'
    })


def voluntario_delete(request, id):
    """Ejercicio 9: Eliminar un voluntario con confirmación"""
    voluntario = get_object_or_404(Voluntario, id=id)
    
    if request.method == 'POST':
        nombre = voluntario.nombre
        voluntario.delete()
        messages.success(request, f'Voluntario "{nombre}" eliminado exitosamente.')
        return redirect('voluntario_list')
    
    return render(request, 'voluntario_confirm_delete.html', {'voluntario': voluntario})


# ============ VISTAS DE EVENTOS ============

def evento_list(request):
    """Ejercicio 6: Listado de todos los eventos"""
    eventos = Evento.objects.all().order_by('-fecha')
    return render(request, 'evento_list.html', {'eventos': eventos})


def evento_detail(request, id):
    """Vista detallada de un evento con sus voluntarios"""
    evento = get_object_or_404(Evento, id=id)
    voluntarios = evento.voluntarios.all()
    
    return render(request, 'evento_detail.html', {
        'evento': evento,
        'voluntarios': voluntarios
    })


def evento_create(request):
    """Ejercicio 7: Crear un nuevo evento"""
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento creado exitosamente.')
            return redirect('evento_list')
    else:
        form = EventoForm()
    
    return render(request, 'evento_form.html', {
        'form': form,
        'titulo': 'Nuevo Evento',
        'boton': 'Crear Evento'
    })


def evento_update(request, id):
    """Ejercicio 8: Modificar un evento existente"""
    evento = get_object_or_404(Evento, id=id)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Evento "{evento.titulo}" actualizado exitosamente.')
            return redirect('evento_list')
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'evento_form.html', {
        'form': form,
        'titulo': f'Editar Evento: {evento.titulo}',
        'boton': 'Actualizar Evento'
    })


def evento_delete(request, id):
    """Ejercicio 9: Eliminar un evento con confirmación"""
    evento = get_object_or_404(Evento, id=id)
    
    if request.method == 'POST':
        titulo = evento.titulo
        evento.delete()
        messages.success(request, f'Evento "{titulo}" eliminado exitosamente.')
        return redirect('evento_list')
    
    return render(request, 'evento_confirm_delete.html', {'evento': evento})
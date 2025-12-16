from django import forms
from .models import Voluntario, Evento


class VoluntarioForm(forms.ModelForm):
    """Formulario para crear y editar voluntarios"""
    
    class Meta:
        model = Voluntario
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono'
        }


class EventoForm(forms.ModelForm):
    """Formulario para crear y editar eventos"""
    
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha', 'voluntarios']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada del evento',
                'rows': 4
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'voluntarios': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'fecha': 'Fecha del Evento',
            'voluntarios': 'Voluntarios Asignados'
        }
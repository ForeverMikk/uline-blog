from django import forms
from django.urls import reverse

from .models import (
    Usuario,
    Estudiante,
    Profesor
)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Definimos los campos que se van a mostrar en la forma
        fields = ['nombre','apellido_paterno', 'fecha_nacimiento', 'genero', 'correo']
    
    def __init__(self,*args, **kwargs):
        # Es necesario inicializar la clase padre ModelForm
        super(UsuarioForm,self).__init__(*args,**kwargs)
 
class EstudianteForm(UsuarioForm):
    class Meta:
        model = Estudiante
        # Con esta funcion vas a mostrar los datos del usuario mas la matricula si es profesor
        fields = UsuarioForm.Meta.fields + ['matricula', 'semestre']

class ProfesorForm(UsuarioForm):
    class Meta:
        model = Profesor
        fields = UsuarioForm.Meta.fields + ['matricula', 'materia']
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render

from .models import (
    Usuario,
    Estudiante
)

def funcion1(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({
        'mi_mensaje':'Mi primer template en Django'
    }))
    
def listar_personas(request):
    u = Usuario.objects.all()
    users = {
        'usuarios': u
    }
    return render(request, 'home.html', users)
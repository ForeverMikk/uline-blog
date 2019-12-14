from django.urls import path, include
from .views import funcion1, listar_personas

urlpatterns = [
    path('home/', listar_personas)
]

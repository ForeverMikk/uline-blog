from django.contrib import admin

from .models import (
    Usuario,
    Estudiante,
    Profesor,
    Post
    )

from .forms import (
    UsuarioForm,
    EstudianteForm,
    ProfesorForm
)

class UsuarioTabularAdmin(admin.TabularInline):
    model = Usuario
    extra = 0
    max_num = 1
    form = UsuarioForm

class EstudianteTabularAdmin(UsuarioTabularAdmin):
    fk_name = 'estudiante'
    verbose_name = 'Estudiante'
    verbose_name_plural = 'Estudiante'

class ProfesorTabularAdmin(UsuarioTabularAdmin):
    fk_name = 'profesor'
    verbose_name = 'Profesor'
    verbose_name_plural = 'Profesor'

def enroll_student_matricula(modeladmin, request, queryset):
    for usuario in queryset:
        if not usuario.is_student:
            Estudiante.enroll_student(usuario=usuario)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'apellido_paterno',
        'genero',
        'fecha_nacimiento',
        'correo'
    ]

    search_fields = [ # Aqui definimos los campos que se utilizan para hacer busquedas
        'nombre',
        'apellido_paterno'
    ]

    list_filter = [ # Aqui definimos los campos que se utilizan para hacer filtros
        'apellido_paterno',
        'genero'
    ]

    form = UsuarioForm
    # En el atributo inlines, se definen todas aquellas clases que se utilizan para desplegar o capturar datos de manera
    # mas compleja, como aquellos datos que se encuentran en algun tipo de relación con la clase persona
    inlines = [
        # EstudianteTabularAdmin,
        # ProfesorTabularAdmin
    ]

    actions = [
        enroll_student_matricula
    ]

    def es_estudiante(self, obj):
        return obj.is_student




class EstudianteAdmin(UsuarioAdmin):
    # La clase EstudianteAdmin heredara de la clase UsuarioAdmin, 
    # ya que sus funciones son similares, 
    # con esto se logra reducir el numero de lineas de codigo y de metodos a implementar,
    list_display = UsuarioAdmin.list_display
    list_filter = UsuarioAdmin.list_filter
    form = EstudianteForm

class ProfesorAdmin(UsuarioAdmin):
    pass


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Post)
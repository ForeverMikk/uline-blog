from django.db import models
from django.utils import timezone

GENERO_CHOICES = [
    ('M', 'MASCULINO'),
    ('F', 'FEMENINO')
]

SEMESTRE = [
    ('1','Primero'),
    ('2','Segundo'),
    ('3','Tercero'),
    ('4','Cuarto'),
    ('5','Quinto'),
    ('6','Sexto'),
    ('7','Septimo'),
    ('8','Octavo'),
    ('9','Noveno')
]

class Usuario(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido_paterno = models.CharField(max_length=30, null=False, blank=False)
    fecha_nacimiento = models.DateTimeField(null=False, blank=False)    
    genero = models.CharField(max_length=1, null=False, blank=False, choices=GENERO_CHOICES)
    correo = models.CharField(max_length=30, null=False, blank=False)

    #Esta funcion va a mosrtar esos datos del usuario en la BD, si no va a colocar "Object...."
    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido_paterno)

    @property
    def is_student(self):
        return Estudiante.objects.filter(usuario=self).first() is not None

class Post(models.Model):
    autor = models.ForeignKey(Usuario, related_name='user_blog',on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=False, blank=False)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion =  models.DateTimeField(blank=True, null=True)

    def publicacion(self):
        self.fecha_publicacion = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo

class Estudiante(Usuario):
    usuario = models.ForeignKey(Usuario, related_name='rel_from_est' ,on_delete=models.CASCADE)
    matricula = models.CharField(max_length=10, null=False, blank=False)
    semestre = models.CharField(max_length=30, null=False, blank=False, choices=SEMESTRE)
    carrera = models.CharField(max_length=100,null=False, blank=False)

    def __str__(self):
        return "{} {} {}".format(self.nombre, self.apellido_paterno, self.matricula)
    
    @classmethod
    def new_matricula(cls):
        # Funcion que calcula la siguiente matricula en base a la ultima matricula asignada
        if cls.objects.all().count() == 0:
            return "00001"
        else:
            matriculas = cls.objects.all().order_by('-matricula').values_list('matricula', flat=True)
            ultima_matricula_string = matriculas[0]
            ultima_matricula = int(ultima_matricula_string)
            ultima_matricula += 1
            ultima_matricula_string = str(ultima_matricula)
            siguiente_matricula_string = "{}{}".format(
                "0" * (5 - len(ultima_matricula_string)),
                ultima_matricula_string
            )
            return siguiente_matricula_string        

    def save(self, *args, **kwargs):
        matricula = getattr(self, 'matricula', None)
        if matricula is None or len(matricula.strip()) == 0:
            self.matricula = self.__class__.new_matricula()
        super(Estudiante, self).save(*args, **kwargs)

    @classmethod
    def enroll_student(cls, usuario):
        if usuario is not None:
            estudiante = cls(usuario=usuario)
            for name, value in vars(usuario).items():
                setattr(estudiante, name, value)
            estudiante.save()
            return estudiante
        return None


class Profesor(Usuario):
    usuario = models.ForeignKey(Usuario,related_name='rel_from_prof', on_delete=models.CASCADE)
    matricula = models.CharField(max_length=10, null=False, blank=False)
    materia = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return "{} {} {}".format(self.nombre, self.apellido_paterno, self.matricula)
    
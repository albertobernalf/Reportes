from django.db import models

# Create your models here.


class VistaCex(models.Model):

    id = models.AutoField(primary_key=True)
    cita= models.IntegerField()
    fecha= models.DateField(default='2021-01-01')
    hora = models.CharField(max_length=8,default='')
    consultorio= models.IntegerField()
    especialidad= models.CharField(max_length=70)
    medico= models.CharField(max_length=40)
    paciente= models.CharField(max_length=75)
    estado_cita= models.CharField(max_length=10)
    llamada= models.IntegerField()
    atendido= models.IntegerField()


    def __str__(self):
        return self.paciente

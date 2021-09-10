from django.db import models

# Create your models here.


class UsuariosHc(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=30)
    contrasena = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)



    def __str__(self):
        return self.nombre

class ContratosHc(models.Model):
        id = models.AutoField(primary_key=True)
        mpmeni = models.CharField(max_length=15)
        menomb = models.CharField(max_length=30)



        def __str__(self):
            return self.menomb


class UsusariosContratosHc(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=30)
    mpmeni = models.CharField(max_length=15)
    estado =models.CharField(max_length=1)

    def __str__(self):
        return self.usuario
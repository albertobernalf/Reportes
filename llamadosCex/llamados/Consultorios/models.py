from django.db import models

# Create your models here.


class Consul(models.Model):

    id = models.AutoField(primary_key=True)
    conscod= models.IntegerField()
    consdet= models.CharField(max_length=70,default='')
    adicional = models.IntegerField()

    def __str__(self):
        return self.consdet

class CamposSelect(models.Model):
    id_consultorio =models.ForeignKey('Consul', default=1, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.id
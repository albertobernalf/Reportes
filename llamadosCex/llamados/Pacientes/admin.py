from django.contrib import admin

# Register your models here.
from Pacientes.models import VistaCex

class vistaCexAdmin(admin.ModelAdmin):

        list_display = ("cita","paciente","medico" ,"fecha","hora","consultorio","especialidad")
        search_fields = ("cita","paciente","medico", "fecha","hora","consultorio","especialidad")

admin.site.register(VistaCex, vistaCexAdmin)
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import VistaCex
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError


class VistaCexForm(forms.ModelForm):
    model = VistaCex

    id = forms.IntegerField()
    cita = forms.FloatField()
    fecha = forms.DateField()
    hora = forms.CharField()
    consultorio = forms.FloatField()
    especialidad = forms.CharField()
    medico = forms.CharField()
    paciente = forms.CharField()
    estado_cita = forms.CharField()
    llamada = forms.IntegerField()
    atendido = forms.IntegerField()

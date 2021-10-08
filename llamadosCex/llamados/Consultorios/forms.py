from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from Consultorios.models import Consul, CamposSelect
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError


class ConsulForm(forms.ModelForm):
    class Meta:
        model = Consul
        fields = ['conscod','consdet']


        id = forms.IntegerField()
        conscod = forms.IntegerField()
        consdet = forms.CharField()
        adicional = forms.IntegerField()

class CamposSelectForm(forms.ModelForm):

    class Meta:
        model = CamposSelect
        fields = '__all__'

        id_consultorio = forms.ModelChoiceField(queryset=Consul.objects.all().order_by('consdet'))

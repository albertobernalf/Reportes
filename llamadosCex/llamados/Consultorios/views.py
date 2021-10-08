from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView, CreateView, TemplateView
from Consultorios.models import Consul
from Consultorios.forms import ConsulForm, CamposSelectForm
from Pacientes.models import VistaCex
from Pacientes.forms import VistaCexForm
from django.shortcuts import render, redirect, HttpResponse
import json
from django.http import JsonResponse


def DespliegaConsultorio(request):
    conscod = request.POST["conscod"]
    vistaCex = VistaCex.objects.raw('SELECT * FROM Pacientes_VistaCex where consultorio=140')
    context = {}
    context['VistaCex'] = vistaCex
    context['form'] = VistaCexForm
    print("Me voy a la vista")
    return render(request, "consultorios.html", context)
	




class IngresoConsultorios(TemplateView):
    print("Encontre")
    template_name = 'consul1.html'

    def get_context_data(self, **kwargs):
        print("Entre a Contexto")
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'
        context['form'] = CamposSelectForm
        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST, por el camino del SAVE ")
        print(request.POST["id_consultorio"])
        conscod = request.POST["id_consultorio"]
        fila = Consul.objects.get(id=request.POST["id_consultorio"])
        print (fila.conscod)
        seleccion = 'SELECT * FROM Pacientes_VistaCex where atendido=0 and consultorio=' + str(fila.conscod)
        print (seleccion)
        vistaCex = VistaCex.objects.raw(seleccion)
        print (vistaCex)
        context = {}
        context['VistaCex'] = vistaCex
        context['form'] = VistaCexForm
        print("Me voy a la vista1")
        return render(request, "consultoriosP.html", context)

def Modal(request, cita):
    if request.method == 'POST':
        print ("Entre POST de Modal")
        return null

    print("Entre Modal findOne")
    print(cita)
    vistaCex = VistaCex.objects.get(cita = cita)
    cita1 = vistaCex.cita
    medico = vistaCex.medico
    consultorio = vistaCex.consultorio
    fecha = vistaCex.fecha
    print(vistaCex.cita)
    print(vistaCex.medico)
    datos = {"cita1": vistaCex.cita, "consultorio":vistaCex.consultorio, "medico":vistaCex.medico,"fecha":vistaCex.fecha, "hora":vistaCex.hora, "paciente":vistaCex.paciente,"llamada":vistaCex.llamada,"atendido":vistaCex.atendido,"estado_cita":vistaCex.estado_cita}
    print("De regreso")
    print(vistaCex)
    #return HttpResponse(json.dumps(vistaCex))
    #return HttpResponse(vistaCex)
    return JsonResponse(datos)


def Save(request):
    print("entre a grabar METODO SAVE")
    print(request)
    cita = request.POST["cita"]
    llamada = request.POST["llamada"]
    atendido = request.POST["atendido"]
    vistaCex = VistaCex.objects.get(cita=cita)
    print(cita)
    print(llamada)
    print(atendido)
    vistaCex.llamada=llamada
    vistaCex.atendido=atendido
    vistaCex.save()

    return HttpResponse("ok")

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, TemplateView
from django.shortcuts import render, redirect, HttpResponse
import json
from django.http import JsonResponse
import pyodbc


def DespliegaConsultorio(request):
    #conscod = request.POST["conscod"]
    vistaCex = VistaCex.objects.raw('SELECT * FROM Pacientes_VistaCex where consultorio=140')
    context = {}
    context['VistaCex'] = vistaCex
    #context['form'] = VistaCexForm
    print("Me voy a la vista")
    return render(request, "consultorios.html", context)



class IngresoConsultorios(TemplateView):
    print("Encontre")
    template_name = 'consul1.html'

    def get_context_data(self, **kwargs):
        print("Entre a Contexto")

        con1 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        cursor = con1.cursor()
        cursor.execute(
            "SELECT  conscod conscod, consdet consdet FROM HOSVITAL.CONSUL  where conscod in (select consultorio from hosvital.vistacex  where fecha = current_date AND atendido=0) ORDER BY CONSDET")
        rows = cursor.fetchall()
        Consul  = []

        for row in rows:
            print(row.CONSCOD, row.CONSDET)
            Consul.append({'CONSCOD': row.CONSCOD, 'CONSDET': row.CONSDET})
        print(Consul )
        con1.close()

        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'

        context['Consul'] = Consul
        context['form'] = Consul
        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST, por el camino del SAVE ")
        print(request)
        #print(request.POST["CONSCOD"])
        conscod = request.POST["seleccion"]
        print("valor para CONSCOD = ")
        print (conscod)
        #conscod=140
        con2 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cursor = con2.cursor()
        seleccion = 'SELECT * FROM HOSVITAL.VistaCex where fecha = current_date and atendido=0 and consultorio=' + str(conscod)
        cursor.execute(seleccion)
        rows = cursor.fetchall()
        vistaCex = []

        for row in rows:
            print(row.CITA, row.PACIENTE)
            vistaCex.append({'CITA': row.CITA, 'FECHA': row.FECHA, 'HORA': row.HORA, 'CONSULTORIO': row.CONSULTORIO,
                             'ESPECIALIDAD': row.ESPECIALIDAD,
                             'MEDICO': row.MEDICO,
                             'PACIENTE': row.PACIENTE, 'ESTADO_CITA': row.ESTADO_CITA, 'LLAMADA': row.LLAMADA,
                             'ATENDIDO': row.ATENDIDO})

        print(vistaCex)
        con2.close()
        context = {}
        context['VistaCex'] = vistaCex
        #context['form'] = VistaCexForm
        print("Me voy a la vista1")

        return render(request, "consultoriosP.html", context)


def Modal(request, cita):
    if request.method == 'POST':
        print ("Entre POST de Modal")
        return null

    print("Entre Modal findOne")
    print(cita)

    con3 = pyodbc.connect(
        'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cursor = con3.cursor()
    seleccion = 'SELECT * FROM HOSVITAL.VistaCex where cita =' + str(cita)
    cursor.execute(seleccion)
    rows = cursor.fetchall()
    for row in rows:
        print(row.CITA, row.PACIENTE)
        datos = {"cita1": row.CITA, "consultorio": row.CONSULTORIO, "medico": row.MEDICO,
                 "fecha": row.FECHA, "hora": row.HORA, "paciente": row.PACIENTE, "llamada": row.LLAMADA,
                 "atendido": row.ATENDIDO, "estado_cita": row.ESTADO_CITA}

    print(datos)
    con3.close()
    print("De regreso")


    return JsonResponse(datos)


def Save(request):
        print("entre a grabar METODO SAVE")
        print(request)
        cita = request.POST["cita"]
        llamada = request.POST["llamada"]
        atendido = request.POST["atendido"]

        con4 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cursor = con4.cursor()
        seleccion = 'UPDATE HOSVITAL.VistaCex SET llamada = ' + str(llamada) + ', atendido= ' + str(atendido) + ' where cita =' + str(cita)
        cursor.execute(seleccion)
        con4.commit()
        con4.close()

        return HttpResponse("ok")


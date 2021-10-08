from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView, CreateView, TemplateView
from Pacientes.models import VistaCex
from Pacientes.forms import VistaCexForm
import pyodbc

class ViewCex(TemplateView):
    template_name = 'llamados.html'

    def get_context_data(self, **kwargs):

        print("Entre Contexto")
        context = super().get_context_data(**kwargs)

        con1 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        cursor = con1.cursor()
        cursor.execute(
            "SELECT v.cita cita, v.fecha fecha,v.hora hora,v.consultorio consultorio,c.consdet nombre_consultorio, v.especialidad especialidad, v.medico medico, v.paciente  paciente ,v.estado_cita estado_cita, v.llamada llamada,v.atendido atendido FROM VistaCex v inner join consul c on (c.conscod = v.consultorio) where v.fecha = current_date and v.atendido=0")
        rows = cursor.fetchall()
        data = []

        for row in rows:
            print(row.CITA, row.PACIENTE)
            data.append({'CITA': row.CITA, 'FECHA': row.FECHA, 'HORA': row.HORA, 'CONSULTORIO': row.CONSULTORIO,
                         'NOMBRE_CONSULTORIO': row.NOMBRE_CONSULTORIO, 'ESPECIALIDAD': row.ESPECIALIDAD,
                         'MEDICO': row.MEDICO,
                         'PACIENTE': row.PACIENTE, 'ESTADO_CITA': row.ESTADO_CITA, 'LLAMADA': row.LLAMADA,
                         'ATENDIDO': row.ATENDIDO})
        print(data)


        context['title'] = 'Mi gran Template'
        #vistaCex = VistaCex.objects.raw('SELECT * FROM Pacientes_VistaCex')
        #context['VistaCex'] = vistaCex
        context['VistaCex'] = data
        context['form'] = VistaCexForm

        return context

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            print("Entre Contexto")
            context = super().get_context_data(**kwargs)
            context['title'] = 'Mi gran Template'
            vistaCex = VistaCex.objects.raw('SELECT * FROM Pacientes_VistaCex')
            context['VistaCex'] = vistaCex
            context['form'] = VistCexForm

            return context

        if request.is_ajax():
            try:
                data = []
                for d in VistaCex.objects.all():
                    data.append({})

            except Exception as e:
                print("Exception")

                return HttpResponse(json.dumps(data))



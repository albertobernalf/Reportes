from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView, CreateView, TemplateView
from Pacientes.models import VistaCex
from Pacientes.forms import VistaCexForm


class ViewCex(TemplateView):
    template_name = 'llamados.html'

    def get_context_data(self, **kwargs):

        print("Entre Contexto")
        context = super().get_context_data(**kwargs)

        context['title'] = 'Mi gran Template'
        vistaCex = VistaCex.objects.raw('SELECT * FROM Pacientes_VistaCex')
        context['VistaCex'] = vistaCex
        context['form'] = VistaCexForm

        return context

    def post(self, reques, *args, **kwargs):

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



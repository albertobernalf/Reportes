from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pyodbc
from django.views.generic import CreateView, TemplateView, ListView, View

# Create your views here.

class ContratosView(TemplateView):

    print("Entre Clase TempView")
    template_name = 'inicio8.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contratos Usuario'
        myConexion = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cur = myConexion.cursor()
        cur.execute("SELECT mpmeni, menomb  FROM hosvital.contratoshc order by menomb")
        ContratosHc = []

        for mpmeni, menomb in cur.fetchall():
            ContratosHc.append({'mpmeni': mpmeni, 'menomb': menomb})

        myConexion.close()
        context['ContratosHc'] = ContratosHc

        print(ContratosHc)

        miConexion1 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cur1 = myConexion1.cursor()
        comando = "SELECT u.usuario usuario,u.nombre nombre, c.mpmeni cod_contrato, c.menomb contrato FROM hosvital.usuarioscontratoshc r, hosvital.usuarioshc u, hosvital.contratoshc c WHERE r.mpmeni=c.mpmeni and r.usuario = u.usuario order by u.usuario "
        cur1.execute(comando)

        usuariosHc = []

        for usuario, nombre, cod_contrato, contrato in cur1.fetchall():
            usuariosHc.append(
                {'usuario': usuario, 'nombre': nombre, 'cod_contrato': cod_contrato, 'contrato': contrato})
            print(usuario)

        myConexion1.close()

        context = {}


        context['UsuariosHc'] = usuariosHc


        return context
    
    def post(self, request, *args, **kwargs ):
        print("entre post")
        usuario = request.POST.get('usuario')
        print(usuario)

        myConexion2 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cur2 = myConexion2.cursor()
        comando = "SELECT u.usuario usuario,u.nombre nombre, c.mpmeni cod_contrato, c.menomb contrato FROM hosvital.ususarioscontratoshc r, hosvitl.usuarioshc u, hosvital.contratoshc c WHERE r.mpmeni=c.mpmeni and r.usuario = u.usuario and u.usuario='" + usuario + "'"
        cur2.execute(comando)

        usuariosHc=[]

        for usuario,  nombre, cod_contrato, contrato in cur2.fetchall():
            usuariosHc.append({'usuario': usuario,  'nombre': nombre,'cod_contrato' : cod_contrato, 'contrato' : contrato})
            print(usuario)

        myConexion2.close()

        context = {}

        context['UsuariosHc'] = usuariosHc

        myConexion3 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cur3 = myConexion3.cursor()
        cur3.execute("SELECT mpmeni, menomb  FROM hosvital.contratoshc order by menomb")
        ContratosHc = []

        for mpmeni, menomb in cur3.fetchall():
            ContratosHc.append({'mpmeni': mpmeni, 'menomb': menomb})

        myConexion3.close()
        context['ContratosHc'] = ContratosHc


        return render (request, "inicio8.html", context)


def eliminarContrato(request, usuario, cod_contrato):
    print("EntreBorrar Contrato")
    print(usuario)
    print(cod_contrato)
    miConexion4 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur4 = miConexion4.cursor()
    comando = "delete FROM hosvital.usuariosContratoshc WHERE usuario = '" + str(usuario) + "' and mpmeni = '" + str(cod_contrato.strip())  + "'"
    print(comando)
    cur4.execute(comando)
    miConexion4.commit()
    miConexion4.close()
    dato = 'Contrato Borrado !'


    myConexion5 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur5 = myConexion5.cursor()
    comando = "SELECT u.usuario usuario,u.nombre nombre, c.mpmeni cod_contrato, c.menomb contrato FROM hosvital.ususarioscontratoshc r, hosvital.usuarioshc u, hosvital.contratoshc c WHERE r.mpmeni=c.mpmeni and r.usuario = u.usuario and u.usuario='" + usuario + "'"
    cur5.execute(comando)

    usuariosHc = []

    for usuario, nombre, cod_contrato, contrato in cur4.fetchall():
        usuariosHc.append({'usuario': usuario, 'nombre': nombre, 'cod_contrato': cod_contrato, 'contrato': contrato})
        print(usuario)

    myConexion5.close()

    context = {}

    context['UsuariosHc'] = usuariosHc

    myConexion6 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur6 = myConexion6.cursor()
    cur6.execute("SELECT mpmeni, menomb  FROM hosvital.contratoshc order by menomb")
    ContratosHc = []

    for mpmeni, menomb in cur6.fetchall():
        ContratosHc.append({'mpmeni': mpmeni, 'menomb': menomb})

    myConexion6.close()
    context['ContratosHc'] = ContratosHc

    return render(request, "inicio8.html", context)


def grabarContrato(request, usuario, cod_contrato):
    print("Entre Grabar Contrato")
    usuario = request.POST.get('usuario')
    cod_contrato = request.POST.get('cod_contrato')
    print(usuario)
    print(cod_contrato)
    miConexion7 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur7 = miConexion7.cursor()
    comando = "insert into hosvital.usuariosContratoshc  (usuario, mpmeni, estado) values ('" + str(usuario) + "' , '" + str(cod_contrato) + "' , 'A')"
    print(comando)
    cur7.execute(comando)
    miConexion7.commit()
    miConexion7.close()
    dato = 'Contrato Adicionado !'


    myConexion8 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur8 = myConexion8.cursor()
    comando = "SELECT u.usuario usuario,u.nombre nombre, c.mpmeni cod_contrato, c.menomb contrato FROM hosvital.usuarioscontratoshc r, hosvital.usuarioshc u, hosvital.contratoshc c WHERE r.mpmeni=c.mpmeni and r.usuario = u.usuario order by u.usuario"
    cur8.execute(comando)

    usuariosHc = []

    for usuario, nombre, cod_contrato, contrato in cur8.fetchall():
        usuariosHc.append({'usuario': usuario, 'nombre': nombre, 'cod_contrato': cod_contrato, 'contrato': contrato})
        print(usuario)

    myConexion8.close()

    context = {}

    context['UsuariosHc'] = usuariosHc

    myConexion9 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur9 = myConexion9.cursor()
    cur9.execute("SELECT mpmeni, menomb  FROM hosvital.contratoshc order by menomb")
    ContratosHc = []

    for mpmeni, menomb in cur9.fetchall():
        ContratosHc.append({'mpmeni': mpmeni, 'menomb': menomb})

    myConexion9.close()
    context['ContratosHc'] = ContratosHc

    return render(request, "inicio8.html", context)


from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, View
from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
import pyodbc



# Create your views here.

class AdmUsuariosView(TemplateView):
    print("Entre Inicio5")
    template_name = 'inicio7.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi Inicio'
        #miConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='hc')
        miConexion = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        comando = "SELECT usuario,contrasena,nombre FROM hosvital.usuarioshc"
        cur = miConexion.cursor()
        #cur.execute("SELECT usuario,contrasena,nombre FROM hosvital.usuarioshc")
        cur.execute(comando)

        #rows = cur.fetchall()
        usuariosHc=[]

        for usuario, contrasena, nombre in cur.fetchall():
            usuariosHc.append({'usuario':usuario,'contrasena':contrasena,'nombre':nombre})
            print(usuario)

        miConexion.close()


        #usuariosHc = UsuariosHc.objects.all()

        context['UsuariosHc'] = usuariosHc

        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST inicio")

        usuario = request.POST.get('usuario');
        contrasena = request.POST.get('contrasena');

        print(usuario)
        print(contrasena)

        #  Arrancamos
        context = {}
        miConexion1 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        comando = "SELECT usuario,contrasena,nombre FROM hosvital.usuarioshc"
        cur1 = miConexion1.cursor()
        cur1.execute(comando)

        usuariosHc = []

        for usuario, contrasena, nombre in cur1.fetchall():
            usuariosHc.append({'usuario':usuario,'contrasena':contrasena,'nombre':nombre})

        print(usuario)

        miConexion1.close()

        #usuariosHc = UsuariosHc.objects.all()

        context['UsuariosHc'] = usuariosHc

        return render(request, "inicio7.html", context)

def Modal (request, usuario, contrasena, nombre):

        print("Entre a Modal")
        print(usuario)
        print(contrasena)
        print(nombre)
        miConexion2 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cur2 = miConexion2.cursor()
        comando= "SELECT usuario,contrasena,nombre FROM hosvital.usuarioshc WHERE usuario = '" + str(usuario) + "'"
        print (comando)
        cur2.execute(comando)

        UsuariosHc = {}

        for usuario, contrasena, nombre in cur2.fetchall():
            UsuariosHc ={'usuario': usuario, 'contrasena': contrasena, 'nombre': nombre}

        miConexion2.close()
        print(UsuariosHc)
        return JsonResponse(UsuariosHc,  safe=False)
        #return HttpResponse(UsuariosHc)


def grabar1(request, usuario, contrasena, nombre):
    print("Entre a grabar1")
    usuario1 = request.POST["usuario"]
    contrasena1 = request.POST["contrasena"]
    nombre1 = request.POST["nombre"]
    print(usuario1)
    print(contrasena1)
    print(nombre1)

    miConexion11 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur11 = miConexion11.cursor()
    comando = "SELECT usuario,contrasena,nombre FROM hosvital.usuarioshc WHERE usuario = '" + str(usuario1) + "'"
    print(comando)
    cur11.execute(comando)

    UsuariosHc = []

    for usuario, contrasena, nombre in cur11.fetchall():
        UsuariosHc.append({'usuario': usuario, 'contrasena': contrasena, 'nombre': nombre})

    miConexion11.close()

    if UsuariosHc == []:

         miConexion3 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
         cur3 = miConexion3.cursor()
         comando = "insert into hosvital.usuarioshc (usuario, contrasena, nombre) values ('" + str(usuario1) + "' , '" + str(contrasena1) + "', '" + str(nombre1) + "')"
         print(comando)
         cur3.execute(comando)
         miConexion3.commit()
         miConexion3.close()
         return HttpResponse("Usuario Ingresado ! ")

    else:
        miConexion3 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cur3 = miConexion3.cursor()
        comando = "update hosvital.usuarioshc set usuario = '" + usuario1 + "', contrasena = '" + contrasena1 + "', nombre= '" + nombre1 + "' where usuario = '" + str(
         usuario1) + "'"
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        miConexion3.close()

        return HttpResponse("Usuario Actualizado ! ")
        print("CHAO")

def borrarUsuario(request, usuario):

    print("EntreBorrar Usuario")
    print(usuario)
    miConexion4 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur4 = miConexion4.cursor()
    comando = "delete FROM hosvital.usuarioshc WHERE usuario = '" + str(usuario) + "'"
    print(comando)
    cur4.execute(comando)
    miConexion4.commit()
    miConexion4.close()
    dato = 'Usuario Borrado !'
    miConexion0 = pyodbc.connect('DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cur0 = miConexion0.cursor()
    cur0.execute("SELECT usuario,contrasena,nombre FROM hosvital.usuarioshc")
    # rows = cur.fetchall()
    usuariosHc = []

    for usuario, contrasena, nombre in cur0.fetchall():
        usuariosHc.append({'usuario': usuario, 'contrasena': contrasena, 'nombre': nombre})
        print(usuario)

    miConexion0.close()

    # usuariosHc = UsuariosHc.objects.all()
    context = {}
    context['UsuariosHc'] = usuariosHc

    return render(request, "inicio7.html", context)



def adicionarUsuario(request):
    print("Entre Adicicionar")


def pruebasGit(request):
    print("hola")
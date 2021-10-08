from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView
from django.shortcuts import render, redirect, HttpResponse
import json
from django.http import JsonResponse
import pyodbc


class Traslados(TemplateView):
    print("Encontre")
    template_name = 'Pabellones.html'

    def get_context_data(self, **kwargs):
        print("Entre a Contexto")

        con1 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        cursor = con1.cursor()
        cursor.execute(
            "SELECT  mpcodp mpcodp, mpnomp mpnomp FROM HOSVITAL.MAEPAB order by mpcodp")
        rows = cursor.fetchall()
        Pabellones  = []

        for row in rows:
             Pabellones.append({'MPCODP': row.MPCODP, 'MPNOMP': row.MPNOMP})
        print(Pabellones )
        con1.close()

        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'

        context['Pabellones'] = Pabellones
        #context['form'] = Consul
        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST, por el camino del SAVE ")
        print(request)
        mpcodp = request.POST["seleccion"]
        print("valor para mpcodp = ")
        print (mpcodp)
        con2 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cursor = con2.cursor()
        seleccion = "SELECT V.MPCODP MPCODP, V.MPNUMC MPNUMC, CASE WHEN V.MPDISP =1 THEN 'OCUPADO' WHEN V.MPDISP =0 THEN 'LIBRE' WHEN V.MPDISP =8 THEN 'EN MANT.' ELSE 'NOSABE' END MPDISP,V.MPUCED MPUCED,V.MPUDOC MPUDOC, cap.MPNOMC MPNOMC, DAY(V.MPFCHI)||'/'||MONTH(V.MPFCHI)||'/'||YEAR(V.MPFCHI) MPFCHI ,(DAYS(CURRENT_DATE) - DAYS(V.MPFCHI))  ESTANCIA, V.OBSERVACIONES OBSERVACIONES FROM HOSVITAL.Vistatraslados V LEFT JOIN HOSVITAL.CAPBAS cap ON  (cap.MPTDOC= V.MPUDOC and cap.MPCEDU=V.MPUCED ) "\
                    "INNER JOIN HOSVITAL.MAEPAB1 MPAB1 ON (MPAB1.MPCODP=V.MPCODP AND MPAB1.MPNUMC=V.MPNUMC AND MPAB1.MPACTCAM != 'S' ) "\
                    "where V.MPCODP = " + mpcodp + " ORDER BY V.MPNUMC"
        cursor.execute(seleccion)
        rows = cursor.fetchall()
        Traslados = []

        for row in rows:
            if row.MPNOMC == None :
                Traslados.append({'MPCODP': row.MPCODP, 'MPNUMC': row.MPNUMC, 'MPDISP': row.MPDISP,
                                  'MPUCED': '', 'MPUDOC': '', 'MPNOMC': '',
                                  'MPFCHI': '', 'ESTANCIA': '' , 'OBSERVACIONES': row.OBSERVACIONES})
            else:

                Traslados.append({'MPCODP': row.MPCODP, 'MPNUMC': row.MPNUMC, 'MPDISP': row.MPDISP,
                              'MPUCED': row.MPUCED,'MPUDOC':row.MPUDOC,'MPNOMC' : row.MPNOMC,'MPFCHI': row.MPFCHI,
                              'ESTANCIA':row.ESTANCIA, 'OBSERVACIONES': row.OBSERVACIONES})

        print(Traslados)
        con2.close()
        context = {}
        context['Traslados'] = Traslados
        #context['form'] = VistaCexForm
        print("Me voy a la vista1")

        return render(request, "traslados.html", context)

def Modal(request, MPCODP,  MPNUMC):
    if request.method == 'POST':
        print ("Entre POST de Modal")
        return null

    print("Entre Modal findOne")
    print(MPCODP)
    print(MPNUMC)

    con3 = pyodbc.connect(
        'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
    cursor = con3.cursor()

    seleccion = "SELECT V.MPCODP MPCODP, V.MPNUMC MPNUMC, CASE WHEN V.MPDISP =1 THEN 'OCUPADO' WHEN V.MPDISP =0 THEN 'LIBRE' WHEN V.MPDISP =8 THEN 'EN DESINDECCION' ELSE 'NOSABE' END MPDISP,V.MPUCED MPUCED,V.MPUDOC MPUDOC, cap.MPNOMC MPNOMC, V.MPFCHI MPFCHI ,(DAYS(CURRENT_DATE) - DAYS(V.MPFCHI))  ESTANCIA, V.OBSERVACIONES OBSERVACIONES FROM HOSVITAL.Vistatraslados V LEFT JOIN HOSVITAL.CAPBAS cap ON  (cap.MPTDOC= V.MPUDOC and cap.MPCEDU=V.MPUCED ) " \
                "where V.MPCODP = " + MPCODP + " AND  V.MPNUMC = '" + str(MPNUMC) + "'"


    cursor.execute(seleccion)
    rows = cursor.fetchall()
    for row in rows:
        datos = {"MPCODP" :row.MPCODP,"MPNUMC": row.MPNUMC, "MPDISP": row.MPDISP, "MPUDOC": row.MPUDOC,
                 "MPUCED": row.MPUCED, "MPNOMC": row.MPNOMC, "MPFCHI": row.MPFCHI, "ESTANCIA": row.ESTANCIA,
                 "OBSERVACIONES": row.OBSERVACIONES}

    print(datos)
    con3.close()
    print("De regreso")


    return JsonResponse(datos)


def Save(request, MPNUMC, observaciones, mpcodp):
        print("entre a grabar METODO SAVE")

        MPNUMC = request.POST["MPNUMC"]
        observaciones = request.POST["observaciones"]
        mpcodp = request.POST["mpcodp"]
        print (MPNUMC)
        print(observaciones)
        print(mpcodp)

        con4 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cursor = con4.cursor()
        seleccion = "UPDATE HOSVITAL.VistaTraslados SET observaciones = '" + observaciones + "' where mpcodp = " + str(mpcodp) +     " and MPNUMC = '" + str(MPNUMC) + "'"
        cursor.execute(seleccion)
        con4.commit()
        con4.close()

        return HttpResponse("ok")


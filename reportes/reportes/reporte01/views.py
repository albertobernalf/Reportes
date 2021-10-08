from django.shortcuts import render
import csv
from django.views.generic import ListView, CreateView, TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from reporte01.forms import VistaCexForm  # El formulario que creaste
from reporte01.models import VistaCex
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from django.core import serializers
from io import StringIO
from io import BytesIO
import pyodbc
import itertools
from random import randint
from statistics import mean





class nuevoPdfView(TemplateView):
    print("pdf")
    template_name = 'mitemplate.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'
        return context

    def post(self, request, *args, **kwargs):

        print("Entre POST")
        documento = request.POST.get('documento');
        tipodoc  = request.POST.get('tipodoc');
        print(documento)
        print(tipodoc)

        Desde = request.POST.get('Desde', False);
        Hasta = request.POST.get('Hasta', False);

        Desde = Desde + " 00:00:00"
        Hasta = Hasta + " 23:59:59"
        print (Desde)
        print(Hasta)

        # Trae los folios a listar

        tipodoc = 'CC'
        documento = '20106205'

        con0 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cursort = con0.cursor()
        comando = "select hiscsec from hosvital.hccom1 h1 where  h1.histipdoc='" + tipodoc + "' and h1.hisckey= '" + documento + "' and hisfhorat >= '" + Desde + "' and hisfhorat <= '" + Hasta + "' order by hiscsec"
        print(comando)
        cursort.execute(comando)
        rows = cursort.fetchall()
        Folios = []

        for row in rows:
            folio = row.HISCSEC
            Folios.append(row.HISCSEC)

        con0.close()
        print(Folios[2])


        # Trae el cabezote

        con1 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select cap.mptdoc, cap.mpcedu , cap.mpnomc paciente, maeemp.menomb as empresa ,   maetpa3.mtnomp as afiliado, varchar_format(cap.mpfchn ,'dd/mm/yyyy') as fecha_nacimiento , concat((days(current_date) - days(date(cap.mpfchn)))/365, ' AÑOS') as edad_actual, case when cap.mpsexo='M' then 'Masculino'  when cap.mpsexo='F' then 'Femenino' end  as sexo, cap.MPTipAfi	  as grupo_sanguineo,    case when cap.MPEstC= 'C' THEN 'Casado'      when cap.MPEstC= 'S' THEN 'Soltero'  when cap.MPEstC= 'U' THEN 'Union Libre'  when cap.MPEstC= 'V' THEN 'Viudo'  when cap.MPEstC= 'P' THEN ''  when cap.MPEstC= 'O' THEN ''        ELSE ''        end          as estado_civil,     cap.mptele as telefono,cap.mpdire as direccion,   " \
                  "mb2.mdnomb barrio,mb.mdnomd departamento, mb1.mdnomm municipio, case when ocu.modesc is null then 'NINGUNA' else ocu.modesc " \
                  "end  as ocupacion, case when et.mpdscet is null then 'NO APLICA' else et.mpdscet end etnia, et1.mpdnetn  as grupo_etnico, case " \
                  "when niv.niveddsc is null then 'NO APLIC' else niv.niveddsc end nivel_educativo, ate.ateespdes atencion_especial, " \
                  "dis.discdsc discapacidad, pob.GruPobDes grupo_poblacional, concat(concat(concat(concat(concat(concat(i.ingnmresp, ' '), i.ingnmresp2), ' '), i.ingapres), ' ')," \
                  "i.ingapres2)  as responsable, i.ingtelresp    as telefonoresp, case  when i.ingparresp = 'H' then 'HIJO' " \
                  "when i.ingparresp = 'P' then 'Padre' when i.ingparresp = 'F' then 'Familiar' end as parentesco, i.ingnoac as acompanante, i.ingteac as  telefono_acompanante " \
                  "from hosvital.capbas cap  inner join hosvital.maedmb mb on(mb.mdcodd = cap.mdcodd) inner join hosvital.maedmb1 " \
                  "mb1 on(mb1.mdcodd = mb.mdcodd and mb1.mdcodm = cap.mdcodm) inner join hosvital.maedmb2 mb2 on (mb2.mdcodd = mb1.mdcodd and mb2.mdcodm = mb1.mdcodm and mb2.mdcodb = cap.mdcodb) left " \
                  "join hosvital.etnias et on(et.mpcodet = cap.mpcpetn) left join hosvital.etnias1 et1 on (et1.mpcodet = cap.MPCPEtn) inner " \
                  "join hosvital.ingresos i on (i.mptdoc = cap.mptdoc and i.mpcedu = cap.mpcedu and i.ingcsc = (select  min(i2.ingcsc) " \
                  "from hosvital.ingresos i2 where i2.mptdoc = i.mptdoc and i2.mpcedu = i.mpcedu)) inner join hosvital.maeemp maeemp " \
                  "on(maeemp.mennit = i.ingnit) left join hosvital.nivedu niv on (niv.nivedco = cap.mpnivedu) left join " \
                  "hosvital.maeocu ocu on (ocu.mocodi = cap.MOCodPri) left join hosvital.GruPob pob on (pob.GruPobCod = cap.MPGrPo) " \
                  "left join hosvital.discpac dis on (dis.disccod = cap.MPCodDisc) left join hosvital.ateesp ate on (ate.ateespcod = cap.MPGrEs) " \
                  "inner join hosvital.maepac maepac on (maepac.mptdoc = i.mptdoc and maepac.mpcedu = i.mpcedu and maepac.mennit = i.ingnit) " \
                  "inner join  hosvital.maetpa3 maetpa3 on (maetpa3.mtucod = maepac.mtucod and maetpa3.mtcodp = maepac.mtcodp) where cap.mptdoc = '" + tipodoc + "' and cap.mpcedu = '" + documento + "'"

        print(comando)
        cursor = con1.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Cabezote = []
        data =  []
        Cabezote = [("tipodoc", "documento", "PACIENTE", "EMPRESA", "AFILIADO", "FECHA_NACIMIENTO", "EDAD_ACTUAL", "SEXO",
                 "GRUPO_SANGUINEO", "ESTADO_CIVIL", "DIRECCION", "BARRIO", "DEPARTAMENTO", "MUNICIPIO",
                 "OCUPACION", "ETNIA,GRUPO_ETNICO", "NIVEL_EDUCATIVO", "ATENCION_ESPECIAL", "DISCAPACIDAD", "GRUPO_POBLACIONAL", "RESPONSABLE",
                 "TELEFONORESP", "PARENTESCO", "ACOMPANANTE", "TELEFONO_ACOMPANANTE")]

        for row in rows:
            data.append(
                {tipodoc,documento,row.PACIENTE, row.EMPRESA,
                 row.AFILIADO, row.FECHA_NACIMIENTO, row.EDAD_ACTUAL, row.SEXO,
                 row.GRUPO_SANGUINEO, row.ESTADO_CIVIL, row.DIRECCION, row.BARRIO,
                 row.DEPARTAMENTO,row.MUNICIPIO,row.OCUPACION, row.ETNIA,row.GRUPO_ETNICO, row.NIVEL_EDUCATIVO,
                 row.ATENCION_ESPECIAL, row.DISCAPACIDAD,row.GRUPO_POBLACIONAL, row.RESPONSABLE,
                 row.TELEFONORESP, row.PARENTESCO,row.ACOMPANANTE, row.TELEFONO_ACOMPANANTE})

            Cabezote.append({'TIPODOC': tipodoc, 'DOCUMENTO': documento, 'PACIENTE': row.PACIENTE, 'EMPRESA' :row.EMPRESA, 'AFILIADO':row.AFILIADO ,
                             'FECHA_NACIMIENTO':row.FECHA_NACIMIENTO,'EDAD_ACTUAL':row.EDAD_ACTUAL,'SEXO':row.SEXO,'GRUPO_SANGUINEO':row.GRUPO_SANGUINEO,
                             'ESTADO_CIVIL':row.ESTADO_CIVIL,'DIRECCION':row.DIRECCION,'BARRIO':row.BARRIO,'DEPARTAMENTO':row.DEPARTAMENTO,'MUNICIPIO':row.MUNICIPIO,
                              'OCUPACION':row.OCUPACION,'ETNIA':row.ETNIA,'GRUPO_ETNICO':row.GRUPO_ETNICO,'NIVEL_EDUCATIVO':row.NIVEL_EDUCATIVO,
                              'ATENCION_ESPECIAL':row.ATENCION_ESPECIAL, 'DISCAPACIDAD':row.DISCAPACIDAD,'GRUPO_POBLACIONAL':row.GRUPO_POBLACIONAL,'RESPONSABLE':row.RESPONSABLE,
                              'TELEFONORESP':row.TELEFONORESP,'PARENTESCO':row.PARENTESCO,'ACOMPANANTE':row.ACOMPANANTE,'TELEFONO_ACOMPANANTE':row.TELEFONO_ACOMPANANTE})

        con1.close()
        print(Cabezote)

        #issue_table = Table(Cabezote, colWidths=[doc.width / 3.0] * 3)
        #Story.append(issue_table)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="hola.pdf"'
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont('Helvetica', 10)
        y = 750

        c.drawImage('C:\\EntornosPython\\reportes\\reportes\\static\\images\\logo.jpg', 30 , 730, width=50, height=50)

        c.drawString(180, y, 'FUNDACION HOSPITAL SAN CARLOS')
        y = y - 15
        c.drawString(250, y, '860007373-4')
        c.setFont('Helvetica', 10)
        y = y - 25
        c.drawString(30, y, 'HISTORIA CLINICA NO')
        y = y - 15
        c.drawString(30, y, 'Empresa:')
        c.drawString(300, y, 'Afiliado:')
        y = y - 15
        c.drawString(30, y, 'Fecha Nacimiento:')
        c.drawString(180, y, 'Edad Actual:')
        c.drawString(300, y, 'Sexo:')
        c.drawString(350, y, 'Grupo Sanguineo:')
        c.drawString(450, y, 'Estado Civil:')
        y = y - 15
        c.drawString(30, y, 'Telefono:')
        c.drawString(300, y, 'Direccion:')
        y = y - 15
        c.drawString(30, y, 'Barrio:')
        c.drawString(300, y, 'Departamento:')
        y = y - 15
        c.drawString(30, y, 'Municipio:')
        c.drawString(300, y, 'Ocupacion:')
        y = y - 15
        c.drawString(30, y, 'Etnia:')
        c.drawString(300, y, 'Grupo Etnico:')
        y = y - 15
        c.drawString(30, y, 'Nivel Educativo:')
        c.drawString(300, y, 'Atencion Especial:')
        y = y - 15
        c.drawString(30, y, 'Discapacidad:')
        c.drawString(300, y, 'Grupo Poblacional:')
        c.rect(30, 585, 550, -5)
        y = y - 30
        c.drawString(60, y, 'SEDE DE ATENCION:')
        c.drawString(350, y, 'Edad:')

        c.rect(30, 565, y, -5)
        y = y - 20
        c.drawString(60, y, 'FOLIO:')
        c.drawString(180, y, 'FECHA:')
        c.drawString(300, y, 'TIPO DE ATENCION:')
        c.rect(30, 545, 550, -5)

        export_to_pdf1(Cabezote)

        # Trae Triage

        con2 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando ="select h1.hiscsec as folio,h1.hisfhorat as fecha_folio, 'TRIAGE' AS TRIAGE,  h1.hiscltr as triage, des.hisdesdet as observaciones, h1.hiscltr as clasificacion_triage, " \
                "gpo.diadscgru as triage_prioridad  from hosvital.hccom1 h1 inner join hosvital.hccom1des des " \
                "on (des.histipdoc=h1.histipdoc and des.hisckey=h1.hisckey and des.hiscsec= h1.hiscsec) " \
                "inner join hosvital.gpotria gpo on (gpo.diacodgru = h1.hiscltr) where h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(Folios[2])  + " and h1.fhcindesp='TR'"

        print (comando)
        cursor = con2.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Triage = []

        for row in rows:
            Triage.append(
                {'FOLIO': row.FOLIO, 'FECHA_FOLIO': row.FECHA_FOLIO, 'TRIAGE': row.TRIAGE,'OBSERVACIONES' : row.OBSERVACIONES,
                 'CLASIFICACION_TRIAGE':row.CLASIFICACION_TRIAGE,'TRIAGE_PRIORIDAD':row.TRIAGE_PRIORIDAD})

        con2.close()
        print(Triage)

        # Trae Evoluciones

        con3 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio,h1.hisfhorat fecha, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion, " \
                "case when des1.hisdesatr='HISCMOTCON' then 'MOTIVO DE CONSULTA'  when des1.hisdesatr='FHCOBSTRG' then 'OBSERVACIONES'  when des1.hisdesatr='HISCEXFIS2' then 'EXAMEN FISICO'  when des1.hisdesatr='EVODESA' then 'ANALISIS' " \
                "when des1.hisdesatr='EVODESP' then 'PLAN Y MANEJO' when des1.hisdesatr='EVODESO' then 'OBJETIVO' when des1.hisdesatr='EVODESS' then 'SUBJETIVO' when des1.hisdesatr='HISCREVSI2' then 'REVISION X SISTEMAS' " \
                "when des1.hisdesatr='HISCEXFIS3' then 'EXAMEN FISICO 3' when des1.hisdesatr='HISCEXFIS4' then 'EXAMEN FISICO 4' when des1.hisdesatr='HISCEXFIS5' then 'EXAMEN FISICO 5' when des1.hisdesatr='HISCEXFIS6' then 'EXAMEN FISICO 6' " \
                "when des1.hisdesatr='HISCEXFIS9' then 'EXAMEN FISICO 9' when des1.hisdesatr='HISCEXFI10' then 'EXAMEN FISICO 10' when des1.hisdesatr='HISCEXFI11' then 'EXAMEN FISICO 11' when des1.hisdesatr='HISCEXFI12' then 'EXAMEN FISICO 12' " \
                "when des1.hisdesatr='HISCEXFI13' then 'EXAMEN FISICO 13' when des1.hisdesatr='HISCEXFI14' then 'EXAMEN FISICO 14' when des1.hisdesatr='HISCEXFI15' then 'EXAMEN FISICO 15' when des1.hisdesatr='HISCREVSI4' then 'REVISION 4' " \
                "when des1.hisdesatr='HISCREVSI6' then 'REVISION 6' when des1.hisdesatr='HISCREVSI7' then 'REVISION 7' when des1.hisdesatr='HISCREVSI8' then 'REVISION 8' when des1.hisdesatr='HISCREVSI9' then 'REVISION 9' " \
                "when des1.hisdesatr='HISCREVSI10' then 'REVISION 10' when des1.hisdesatr='HISCREVSI11' then 'REVISION 11' when des1.hisdesatr='HISCREVSI12' then 'REVISION 12' when des1.hisdesatr='HISCREVSI13' then 'REVISION 13' " \
                "when des1.hisdesatr='HISCREVS14' then 'REVISION 14' when des1.hisdesatr='HISCREVSI15' then 'REVISION 15'  END TIPO, des1.hisdesdet as descripcion,   h1.hiscenfact as enfermedad_actual " \
                "from  hosvital.hccom1des des1 left join hosvital.hccom1 h1 on (h1.histipdoc=des1.histipdoc and h1.hisckey=des1.hisckey and h1.hiscsec = des1.hiscsec) " \
                "where des1.histipdoc='" + tipodoc + "' and des1.hisckey='" + documento + "' and des1.hiscsec= " + str(Folios[2]) + " and h1.fhcindesp IN ('GN') union select h1.hiscsec as folio,h1.hisfhorat, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion, " \
                "'EVOLUCION MEDICA' TIPO, H33.evodes as descripcion,   h1.hiscenfact as enfermedad_actual " \
                "from   hosvital.hccom1 h1  left join hosvital.hccom33 h33 on (h33.histipdoc=h1.histipdoc and h33.hisckey=h1.hisckey and h33.hiscsec = h1.hiscsec) " \
                "where h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec=" + str(Folios[2]) + " and h1.fhcindesp IN ('GN')"

        print(comando)
        cursor = con3.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Evoluciones = []

        y = y - 25

        for row in rows:
            y = y - 15
            Evoluciones.append(
                {'FOLIO': row.FOLIO, 'FECHA': row.FECHA, 'TIPO_ATENCION': row.TIPO_ATENCION,
                 'TIPO':row.TIPO, 'DESCRIPCION': row.DESCRIPCION,
                 'ENFERMEDAD_ACTUAL': row.ENFERMEDAD_ACTUAL})

            if row.TIPO=='ANALISIS':

                c.drawString(30, y, 'ANALISIS:')
                c.drawString(160, y, 'analisis...')
            if row.TIPO=='MOTIVO DE CONSULTA':
                c.drawString(30, y, 'MOTIVO DE CONSULTA:')
                c.drawString(160, y, 'Motivo')
            if row.TIPO == 'PLAN Y MANEJO':
               c.drawString(30, y, 'PLAN Y MANEJO:')
               c.drawString(160, y, 'Plan')
            if row.TIPO == 'EXAMEN FISICO':
               c.drawString(30, y, 'EXAMEN FISICO:')
               c.drawString(160, y, 'Exa.Fis')
            if row.TIPO == 'REVISION X SISTEMAS':
               c.drawString(30, y, 'REVISION X SISTEMAS:')
               c.drawString(160, y, 'Revis')
            if row.TIPO == 'EVOLUCION MEDICA':
               c.drawString(30, y, 'EVOLUCION MEDICA:')
               c.drawString(160, y, 'Evol')

        con3.close()
        print(Evoluciones)

        # Trae Diagnosticos

        con4 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  hc.histipdoc,hc.hisckey,hc.hiscsec as folio, hc.hcdxcod cod_dx, m.dmnomb diagnostico  , case when hc.hcdxcls=2 then 'DESCARTADO'  when hc.hcdxcls=1 then 'PRINCIPAL' when hc.hcdxcls=0 then 'RELACIONADO'  END tipo " \
                   "from hosvital.hcdiagn hc inner join hosvital.maedia m on (m.dmcodi= hc.hcdxcod) " \
                    "where hc.histipdoc='" + tipodoc + "' and hc.hisckey = '" + documento + "' and hc.hiscsec = " + str(Folios[2]) + " order by hc.hcdxcls, hc.hccnsdx"

        print(comando)
        cursor = con4.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Diagnosticos = []

        y = y - 25

        for row in rows:
            y = y - 15
            Diagnosticos.append(
                {'TIPODOC': tipodoc, 'DOCUMENTO': documento,'FOLIO': row.FOLIO,'COD_DX':row.COD_DX,'DIAGNOSTICO':row.DIAGNOSTICO,
                 'TIPO':row.TIPO})
            c.drawString(30, y, 'DIAGNOSTICO:')
            c.drawString(160, y, 'Diag...')

        con4.close()
        print(Diagnosticos)

        # Trae Notas de Enfermeria

        con5 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio, h1.hisfhorat as fecha_folio, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion, " \
                  "h33.evodes evolucion,'Nota realizada por:'  nota1 ,maemed1.mmnomm enfermera,concat(concat(cast(h33.evofec as varchar(10)),' '),h33.evohor) fecha " \
                  "from hosvital.hccom1 h1 left join  hosvital.hccom33 h33 on (h33.histipdoc=h1.histipdoc and h33.hisckey=h1.hisckey and h33.hiscsec = h1.hiscsec ) " \
                  "inner join hosvital.maemed1 maemed1 on (maemed1.mmcodm=h33.evomed) " \
                  "where h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(Folios[2]) + " and h1.fhcindesp IN ('EN') order by h1.hiscsec"

        print(comando)
        cursor = con5.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        NotasEnf = []
        y = y - 25

        for row in rows:
            Y  = Y- 15
            NotasEnf.append(
                {'FOLIO': row.FOLIO, 'FECHA_FOLIO': row.FECHA_FOLIO, 'TIPO_ATENCION': row.TIPO_ATENCION,
                  'EVOLUCION':row.EVOLUCION,'NOTA1':row.NOTA1,'ENFERMERA':row.ENFERMERA,'FECHA':row.FECHA})
            c.drawString(30, y, 'NOTAS DE ENFERMERIA:')
            c.drawString(160, y, 'Nota...')
        con5.close()
        print(NotasEnf)

        # Trae Registro Medico

        con6 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  mae.mmnomm MEDICO, mae.mmregm as registro,esp.menome especialidad, mae.mmfirma as ruta_firma " \
                   "from hosvital.hccom1 h1 INNER JOIN HOSVITAL.MaEMED1 MAE on (mae.mmcodm = h1.hiscmmed) " \
                   "inner join hosvital.maeesp esp on (esp.mecode= h1.hcesp) where  h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(Folios[2])

        print(comando)
        cursor = con6.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        registroMed = []
        y = y - 25

        for row in rows:
            y = y - 15
            registroMed.append({'MEDICO': row.MEDICO, 'REGISTRO': row.REGISTRO, 'ESPECIALIDAD': row.ESPECIALIDAD,
                 'RUTA_FIRMA': row.RUTA_FIRMA})
            c.drawString(30, y, 'REGISTRO MEDICO:')
            c.drawString(160, y, 'reg......')

        con6.close()
        print(registroMed)


        # Trae Formulacion

        con7 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  a.hiscsec as folio, h1.hisfhorat fecha,  a.fsmcntdia as cantidad, concat(concat(a.hiscansum , ' ')   , u.unmddes)     as Dosis, a.fsmdscmdc as descripcion,via.viapldsc as via, " \
                  "case when a.hcfsfrh = 99  then 'Infusion Continua'  when a.hcfsfrh = 95 then 'Ahora' when a.hcfsfrh = 93  then 'Dosis Unica'  when a.hcfsfrh = 24 then '24 Horas' when a.hcfsfrh = 12 then '12 Horas'  when a.hcfsfrh = 8 then '8 Horas' when a.hcfsfrh = 6 then '6 Horas' when a.hcfsfrh = 4 then '4 Horas'  when a.hcfsfrh = 91 then '1 Hora'  when a.hcfsfrh = 1 then '1 Hora'   else cast(a.hcfsfrh as varchar(10)) end  as frecuencia, " \
                  "case when a.hcsmstgr = 'O' then 'Nuevo'  when a.hcsmstgr = 'S' then 'Suspendido'   when a.hcsmstgr = 'M' then 'Modificado'   when a.hcsmstgr = 'C' then 'Continuar'   when a.hcsmstgr = 'D' then '' " \
                  "when a.hcsmstgr = 'N' then 'Sin Cambios'     when a.hcsmstgr = 'A' then ''   when a.hcsmstgr = 'N' then 'Nuevo' END ACCION " \
                  "from hosvital.FrmSmns as a inner join hosvital.undmedi u on (u.unmdcod=a.hcsmundcd) inner join hosvital.maeviapl via on (via.viaplcod=a.hcfsvia) " \
                  "inner join hosvital.hccom1 h1 on (h1.histipdoc = a.histipdoc and h1.hisckey=a.hisckey  and h1.hiscsec=a.hiscsec ) " \
                  "where  a.histipdoc='" + tipodoc + "' and a.hisckey='" + documento + "' and a.hiscsec= " + str(Folios[2]) +  " and a.hcsmstgr <> 'X' order by a.hiscsec"

        print(comando)
        cursor = con7.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Formulacion = []
        y = y - 25

        for row in rows:
            y = y - 15
            Formulacion.append(
                {'FOLIO': row.FOLIO, 'FECHA': row.FECHA, 'CANTIDAD': row.CANTIDAD,
                 'DOSIS': row.DOSIS,'DESCRIPCION': row.DESCRIPCION,'VIA': row.VIA,
                 'FRECUENCIA': row.FRECUENCIA,'ACCION': row.ACCION})
            c.drawString(30, y, 'FORMULACION:')
            c.drawString(160, y, 'Formula 1......')

        con7.close()
        print(Formulacion)

        # Trae Registro Medico

        con8 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  mae.mmnomm MEDICO, mae.mmregm as registro,esp.menome especialidad, mae.mmfirma as ruta_firma " \
                  "from hosvital.hccom1 h1 INNER JOIN HOSVITAL.MaEMED1 MAE on (mae.mmcodm = h1.hiscmmed) " \
                  "inner join hosvital.maeesp esp on (esp.mecode= h1.hcesp) where  h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(
            Folios[2])

        print(comando)
        cursor = con8.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        registroMed = []
        y = y - 25

        for row in rows:
            y = y - 15
            registroMed.append(
                {'MEDICO': row.MEDICO, 'REGISTRO': row.REGISTRO, 'ESPECIALIDAD': row.ESPECIALIDAD,
                 'RUTA_FIRMA': row.RUTA_FIRMA})
            c.drawString(30, y, 'REGISTRO MEDICO:')
            c.drawString(160, y, 'reg......')

        con8.close()
        print(registroMed)

        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


def export_to_pdf(data):
    t = canvas.Canvas("grilla-alumnos.pdf", pagesize=A4)
    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15

    #xlist = [x + x_offset for x in [0, 200, 250, 300, 350, 400, 480]]
    xlist = [x + x_offset for x in [0, 60, 110, 160, 210, 270, 330]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        t.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                t.drawString(x + 2, y - padding + 3, str(cell))
        t.showPage()

    t.save()


def export_to_pdf1(Cabezote):
    t = canvas.Canvas("grilla-alumnos.pdf", pagesize=A4)
    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15

    #xlist = [x + x_offset for x in [0, 200, 250, 300, 350, 400, 480]]
    xlist = [x + x_offset for x in [0, 60, 110, 160, 210, 270, 330]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    for rows in grouper(Cabezote, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        t.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                t.drawString(x , y , str(cell))
        t.showPage()

    t.save()


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)
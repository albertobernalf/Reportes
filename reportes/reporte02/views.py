from django.shortcuts import render
import csv
from django.views.generic import ListView, CreateView, TemplateView, View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet , ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
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
#from datascience import *
from reportlab.platypus import *
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from django.conf import settings
import os
from reportlab.lib.fonts import addMapping
from reportlab.lib.colors import (
black,
purple,
white,
yellow
)
import json

from reporte02.models import UsuariosHc, ContratosHc, UsusariosContratosHc


# Create your views here.
class nuevoPdfView(TemplateView):
    print("pdf1")
    template_name = 'mitemplate2.html'
    y=0

    def stylesheet():
        styles = {
            "default": ParagraphStyle(
                "default",
                fontName="Times-Roman",
                fontSize=10,
                leading=12,
                leftIndent=0,
                rightIndent=0,
                firstLineIndent=0,
                alignment=TA_LEFT,
                spaceBefore=0,
                spaceAfter=0,
                bulletFontName="Times-Roman",
                bulletFontSize=10,
                bulletIndent=0,
                textColor=black,
                backColor=None,
                wordWrap=None,
                borderWidth=0,
                borderPadding=0,
                borderColor=None,
                borderRadius=None,
                allowWidows=1,
                allowOrphans=0,
                textTransform=None,  # "uppercase" | "lowercase" |                 None
                endDots=None,
                splitLongWords=1,
            )}
        return styles


    def cabezote(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,  subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        localcabezote = y
        print("Entre Cabezote con y = " , y)


        if localcabezote >= 120  or localcabezote == 0 :
            print("SALTO DE  PAGINA cabezote en y =", y)
            localcabezote = 30
        else:
            localcabezote =  localcabezote + 1
            return localcabezote



        logotipo = "C:\\EntornosPython\\reportes\\reportes\\static\\images\\logo.jpg"
        imagen = Image(logotipo, 1 * inch, 1 * inch)
        Story.append(imagen)

        tbl_data = [
             [Paragraph(str(imagen), headline_mayor3),  Paragraph("FUNDACION HOSPITAL SAN CARLOS:", headline_mayor3), ],
        ]

        tbl = Table(tbl_data, colWidths=[2.05 * cm, 17 * cm])

        Story.append(tbl)
        Story.append(Spacer(1, 2))
        nit = '860007373-4'
        Story.append(Paragraph(nit, headline_mayor3))
        Story.append(Spacer(1, 4))

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
                  "join hosvital.ingresos i on (i.mptdoc = cap.mptdoc and i.mpcedu = cap.mpcedu and i.ingcsc = (select  max(i2.ingcsc) " \
                  "from hosvital.ingresos i2 where i2.mptdoc = i.mptdoc and i2.mpcedu = i.mpcedu)) inner join hosvital.maeemp maeemp " \
                  "on(maeemp.mennit = i.ingnit) left join hosvital.nivedu niv on (niv.nivedco = cap.mpnivedu) left join " \
                  "hosvital.maeocu ocu on (ocu.mocodi = cap.MOCodPri) left join hosvital.GruPob pob on (pob.GruPobCod = cap.MPGrPo) " \
                  "left join hosvital.discpac dis on (dis.disccod = cap.MPCodDisc) left join hosvital.ateesp ate on (ate.ateespcod = cap.MPGrEs) " \
                  "inner join hosvital.maepac maepac on (maepac.mptdoc = i.mptdoc and maepac.mpcedu = i.mpcedu and maepac.mennit = i.ingnit) " \
                  "inner join  hosvital.maetpa3 maetpa3 on (maetpa3.mtucod = maepac.mtucod and maetpa3.mtcodp = maepac.mtcodp) where cap.mptdoc = '" + tipodoc + "' and cap.mpcedu = '" + documento + "'"


        cursor = con1.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()


        Cabezote = [
            ("tipodoc", "documento", "PACIENTE", "EMPRESA", "AFILIADO", "FECHA_NACIMIENTO", "EDAD_ACTUAL", "SEXO",
             "GRUPO_SANGUINEO", "ESTADO_CIVIL", "DIRECCION", "BARRIO", "DEPARTAMENTO", "MUNICIPIO",
             "OCUPACION", "ETNIA,GRUPO_ETNICO", "NIVEL_EDUCATIVO", "ATENCION_ESPECIAL", "DISCAPACIDAD",
             "GRUPO_POBLACIONAL", "RESPONSABLE",
             "TELEFONORESP", "PARENTESCO", "ACOMPANANTE", "TELEFONO_ACOMPANANTE")]

        for row in rows:

            texto = 'HISTORIA CLINICA No '

            tbl_data1 = [
                [Paragraph(str(texto), headline_mayor3),Paragraph(str(tipodoc), headline_mayor3),
                 Paragraph(str(documento), headline_mayor3),Paragraph(str(row.PACIENTE), headline_mayor3),
                 Paragraph("", headline_mayor3)
               ],
            ]

            tbl1 = Table(tbl_data1, colWidths=[4 * cm, 2 * cm , 4 * cm ,7 * cm, 2.2 * cm])

            Story.append(tbl1)
            Story.append(Spacer(1, 1))

            tbl_data = [
                [Paragraph("Empresa:", headline_mayor), Paragraph(str(row.EMPRESA), subtitle_atencion), Paragraph("Afiliado:", headline_mayor), Paragraph(str(row.AFILIADO), subtitle_cabezote)],
                       ]
            tbl = Table(tbl_data)
            Story.append(tbl)

            tbl_data2 = [
                [
                 #Paragraph("", headline_mayor4),
                 Paragraph("Fecha Nacimiento:", headline_mayor4), Paragraph(str(row.FECHA_NACIMIENTO), subtitle_nacimiento),   Paragraph("Edad Actual:", headline_mayor4), Paragraph(str(row.EDAD_ACTUAL), subtitle_nacimiento),
                 Paragraph("Sexo:", headline_mayor4), Paragraph(str(row.SEXO), subtitle_cabezote),  Paragraph("Grupo Sanguineo:", headline_mayor4), Paragraph(str(row.GRUPO_SANGUINEO), subtitle_nacimiento),
                 Paragraph("Estado Civil:", headline_mayor4), Paragraph(str(row.ESTADO_CIVIL), subtitle_nacimiento),
                 Paragraph("", headline_mayor4)
                ]]


            tbl2 = Table(tbl_data2, colWidths=[3.5 * cm, 1.8 * cm, 2.5 * cm, 2 * cm, 1.5 * cm, 2 * cm, 4 * cm, 1 * cm, 2 * cm, 1.5 * cm, 0.9 * cm])

            Story.append(tbl2)


            tbl_data = [
                [Paragraph("Telefono:", headline_mayor), Paragraph(str(row.TELEFONO), subtitle_cabezote),
                 Paragraph("Direccion:", headline_mayor), Paragraph(str(row.DIRECCION), subtitle_cabezote)],
            ]
            tbl = Table(tbl_data)
            Story.append(tbl)


            tbl_data = [
                [Paragraph("Barrio:", headline_mayor), Paragraph(str(row.BARRIO), subtitle_cabezote),
                 Paragraph("Departamento:", headline_mayor), Paragraph(str(row.DEPARTAMENTO), subtitle_cabezote)],
            ]
            tbl = Table(tbl_data)
            Story.append(tbl)


            tbl_data = [
                [Paragraph("Municipio:", headline_mayor), Paragraph(str(row.MUNICIPIO), subtitle_cabezote),
                 Paragraph("Ocupacion:", headline_mayor), Paragraph(str(row.OCUPACION), subtitle_cabezote)],
            ]
            tbl = Table(tbl_data)
            Story.append(tbl)


            tbl_data = [
                [Paragraph("Etnia:", headline_mayor), Paragraph(str(row.ETNIA), subtitle_cabezote),
                 Paragraph("Grupo Etnico:", headline_mayor), Paragraph(str(row.GRUPO_ETNICO), subtitle_cabezote)],
            ]
            tbl = Table(tbl_data)
            Story.append(tbl)



            tbl_data = [
                [Paragraph("Nivel Educativo:", headline_mayor), Paragraph(str(row.NIVEL_EDUCATIVO), subtitle_cabezote),
                 Paragraph("Atencion Especial:", headline_mayor), Paragraph(str(row.ATENCION_ESPECIAL), subtitle_cabezote)],
            ]
            tbl = Table(tbl_data)
            Story.append(tbl)

            tbl_data = [
                [Paragraph("Discapacidad:", headline_mayor), Paragraph(str(row.DISCAPACIDAD), subtitle_cabezote),
                 Paragraph("Grupo Poblacional:", headline_mayor),
                 Paragraph(str(row.GRUPO_POBLACIONAL), subtitle_cabezote)],
            ]
            tbl = Table(tbl_data)
            Story.append(tbl)


            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))

            Story.append(Spacer(1, 2))
            tbl_data = [
                [Paragraph("Responsable:", headline_mayor), Paragraph(str(row.RESPONSABLE), subtitle_cabezote),
                 Paragraph("Telefono:", headline_mayor), Paragraph(str(row.TELEFONORESP), subtitle_cabezote),
                 Paragraph("Parenteseco:", headline_mayor), Paragraph(str(row.PARENTESCO), subtitle_cabezote),
                 Paragraph("", headline_mayor)],
            ]
            tbl = Table(tbl_data, colWidths=[3 * cm, 5 * cm, 3 * cm, 2 * cm, 3 * cm, 2 * cm,1.3 * cm])

            Story.append(tbl)


            tbl_data = [
                [Paragraph("Acompanante:", headline_mayor), Paragraph(str(row.ACOMPANANTE), subtitle_cabezote),
                 Paragraph("Telefono:", headline_mayor), Paragraph(str(row.TELEFONO_ACOMPANANTE), subtitle_cabezote),
                 Paragraph("", headline_mayor),Paragraph("", headline_mayor)
                ],
            ]
            tbl = Table(tbl_data)
            Story.append(tbl)

            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Paragraph(texto1, headline_mayor))


            Story.append(Spacer(1, 2))

        con1.close()

        Cabezote.reverse()
        return localcabezote

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'
        return context

        def post(self, request, *args, **kwargs):
            print("Entre POST")

            documento = request.POST.get('documento');
            tipodoc = request.POST.get('tipodoc');
            print(documento)
            print(tipodoc)

            Desde = request.POST.get('Desde', False);
            Hasta = request.POST.get('Hasta', False);


            Desde = Desde + " 00:00:00"
            Hasta = Hasta + " 23:59:59"


            #  Arrancamos

        Story = []
        buff = io.BytesIO()
        doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=26,   leftMargin=32, topMargin=72, bottomMargin=18)

        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.align = 'CENTER'
        styleBH.fontSize = 6

        estilos = getSampleStyleSheet()

        headline_mayor = estilos["Heading1"]
        headline_mayor.alignment = TA_LEFT
        headline_mayor.leading = 8
        headline_mayor.fontSize = 10
        headline_mayor.fontName = "Helvetica-Bold"
        headline_mayor.spaceAfter = 0
        headline_mayor.spaceBefore = 0

        headline_mayor1 = estilos["Heading5"]
        headline_mayor1.alignment = TA_LEFT
        headline_mayor1.leading =6
        headline_mayor1.fontSize = 8
        headline_mayor1.fontName = "Helvetica-Bold"
        headline_mayor1.spaceAfter = 0
        headline_mayor1.spaceBefore = 0

        headline_mayor2 = estilos["Heading5"]
        headline_mayor2.alignment = TA_LEFT
        headline_mayor2.leading = 7
        headline_mayor2.fontSize =8
        headline_mayor2.fontName = "Helvetica-Bold"
        headline_mayor2.spaceAfter = 0
        headline_mayor2.spaceBefore = 0

        headline_mayor3 = estilos["Heading5"]
        headline_mayor3.alignment = TA_CENTER
        headline_mayor3.leading = 8
        headline_mayor3.fontSize =10
        headline_mayor3.fontName = "Helvetica-Bold"
        headline_mayor3.spaceAfter = 0
        headline_mayor3.spaceBefore = 0

        headline_mayor33 = estilos["Heading5"]
        headline_mayor33.alignment = TA_CENTER
        headline_mayor33.leading = 3
        headline_mayor33.fontSize = 10
        headline_mayor33.fontName = "Helvetica-Bold"
        headline_mayor33.spaceAfter = 0
        headline_mayor33.spaceBefore = 0

        headline_mayor4 = estilos["Heading5"]
        headline_mayor4.alignment = TA_CENTER
        #headline_mayor4.leftIndent= 10
        headline_mayor4.leading = 7
        headline_mayor4.fontSize =9
        headline_mayor4.fontName = "Helvetica-Bold"
        headline_mayor4.spaceAfter = 0
        headline_mayor4.spaceBefore = 0

        subtitle_tipoevol = estilos["Heading2"]
        subtitle_tipoevol.leading = 15
        subtitle_tipoevol.fontSize = 10
        subtitle_tipoevol.fontName = "Times-Roman"
        subtitle_tipoevol.spaceAfter = 0
        subtitle_tipoevol.spaceBefore = 0
        subtitle_tipoevol.alignment = TA_LEFT

        subtitle_atencion = estilos["Heading3"]
        subtitle_atencion.leading =9
        subtitle_atencion.fontSize = 8
        subtitle_atencion.fontName = "Times-Roman"
        subtitle_atencion.spaceAfter = 0
        subtitle_atencion.spaceBefore = 0
        subtitle_atencion.alignment = TA_LEFT

        subtitle_cabezote = estilos["Heading4"]
        subtitle_cabezote.leading = 7
        subtitle_cabezote.fontSize = 8
        subtitle_cabezote.fontName = "Times-Roman"
        subtitle_cabezote.spaceAfter = 0
        subtitle_cabezote.spaceBefore = 0
        subtitle_cabezote.alignment = TA_LEFT

        subtitle_nacimiento = estilos["Heading6"]
        subtitle_nacimiento.leading = 7
        subtitle_nacimiento.fontSize = 8
        subtitle_nacimiento.fontName = "Times-Roman"
        subtitle_nacimiento.spaceAfter = 0
        subtitle_nacimiento.spaceBefore = 0
        subtitle_nacimiento.alignment = TA_LEFT



        estilos.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))
        estilos1 = getSampleStyleSheet()
        estilos1.add(ParagraphStyle(name='Justify_left', alignment=TA_LEFT))
        estilos2 = getSampleStyleSheet()
        estilos2.add(ParagraphStyle(name='Justify_right', alignment=TA_RIGHT))
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="Historia.pdf"'
        response['Content-Disposition'] = 'attachment; filename="' + tipodoc + ' ' + documento + '.pdf"'


        #  Fin arrancamos
        # Trae los folios a listar

        #tipodoc = 'CC'
        #documento = '20106205'

        con0 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cursort = con0.cursor()

        comando = "select h1.hiscsec as folio, h1.hisfhorat as fecha_folio, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion , " \
                   "'FUNDACION HOSPITAL SAN CARLOS' empresa,(days(h1.hisfhorat) - days(date(cap.mpfchn)))/365 edadactual " \
                  "from hosvital.hccom1 h1 INNER JOIN HOSVITAL.CAPBAS CAP ON (CAP.MPTDOC = h1.histipdoc and CAP.MPCEDU = h1.HISCKEY) where h1.histipdoc='" + tipodoc + "' and h1.hisckey= '" + documento + "' and   " \
                  "h1.hisfhorat >= '" + Desde + "' and h1.hisfhorat <= '" + Hasta + "' and h1.fhcindesp not IN ('EN')  " \
                  "UNION select h1.hiscsec as folio, h1.hisfhorat as fecha_folio, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion , " \
                  "'FUNDACION HOSPITAL SAN CARLOS' empresa,(days(current_date) - days(date(cap.mpfchn)))/365 edadactual   "  \
                  "from hosvital.hccom1 h1 INNER join  hosvital.hccom33 h33 on (h33.histipdoc=h1.histipdoc and h33.hisckey=h1.hisckey and h33.hiscsec = h1.hiscsec ) inner join hosvital.maemed1 maemed1 on (maemed1.mmcodm=h33.evomed)  INNER JOIN HOSVITAL.CAPBAS CAP ON (CAP.MPTDOC=h1.HISTIPDOC AND CAP.MPCEDU = h1.HISCKEY)  where h1.histipdoc='" + tipodoc +"' and h1.hisckey= '"  + documento + "' and h1.hisfhorat >= '" + Desde + "' and  h1.hisfhorat <= '" + Hasta + "' and h1.fhcindesp IN ('EN') order by 1"


        cursort.execute(comando)
        rowsGlobal = cursort.fetchall()

        y = 0
        localppal = self.cabezote(doc, y, Story, tipodoc, documento, 0,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento)

        for rowGlobal in rowsGlobal:
            folio = rowGlobal.FOLIO

            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))

            tbl_data1 = [
                [Paragraph("SEDE DE ATENCION:", headline_mayor3), Paragraph("001", subtitle_cabezote),
                 Paragraph(str(rowGlobal.EMPRESA), subtitle_cabezote),
                 Paragraph("Edad:", headline_mayor), Paragraph(str(rowGlobal.EDADACTUAL) + 'Años', subtitle_cabezote),
                 Paragraph("", headline_mayor3)
                 ]]

            tbl = Table(tbl_data1, colWidths=[5 * cm, 2 * cm, 6 * cm, 2 * cm, 2 * cm, 3.8 * cm])

            Story.append(tbl)
            localppal = localppal + 4

            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))



            tbl_data = [
                [Paragraph("FOLIO:", headline_mayor33), Paragraph(str(rowGlobal.FOLIO), headline_mayor33),
                 Paragraph("FECHA:", headline_mayor33),Paragraph(str(rowGlobal.FECHA_FOLIO), headline_mayor33),
                 Paragraph("TIPO DE ATENCION:", headline_mayor33),Paragraph(str(rowGlobal.TIPO_ATENCION), headline_mayor33),
                 Paragraph("", headline_mayor33)],
            ]

            tbl1 = Table(tbl_data, colWidths=[1.5 * cm, 1.5 * cm, 2 * cm, 3.5 * cm, 6 * cm , 2 * cm, 3 * cm])

            Story.append(tbl1)

            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))

            Story.append(Spacer(1, 3))
            localppal = localppal + 4

            Story.append(Spacer(1, 2))
            localppal = localppal + 2
            y= localppal
            localTriage = self.triage  (doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento)
            y = localTriage
            localEvoluciones = self.evoluciones( doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento)
            y = localEvoluciones
            localDiagnosticos= self.diagnosticos(doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento)
            y = localDiagnosticos
            localFormulaciones = self.formulacion(doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento)
            y = localFormulaciones
            # Ojom aqui hay un error y es que imoprime 2 veces la firma del medico triage filtra esto

            localEnf = self.notasEnf(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,  headline_mayor4, subtitle_tipoevol, subtitle_atencion,  subtitle_cabezote, subtitle_nacimiento)
            y = localEnf
            locallaboratorios = self.laboratorios(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,   headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
            y = locallaboratorios
            localRegistro = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,  subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)

            Story.append(Spacer(1, 3))

            y=localRegistro+3

        con0.close()
        doc.build(Story)
        response.write(buff.getvalue())
        buff.close()
        return response



    def triage(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Triage

        print("Entre Triage con y = ", y)

        localTriage = y
        print (localTriage)
        localTriage = self.cabezote(doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 , headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento)

        con2 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio,h1.hisfhorat as fecha_folio, 'TRIAGE' AS TRIAGE,  h1.hiscltr as triage, des.hisdesdet as observaciones, h1.hiscltr as clasificacion_triage, " \
                  "gpo.diadscgru as triage_prioridad  from hosvital.hccom1 h1 inner join hosvital.hccom1des des " \
                  "on (des.histipdoc=h1.histipdoc and des.hisckey=h1.hisckey and des.hiscsec= h1.hiscsec) " \
                  "inner join hosvital.gpotria gpo on (gpo.diacodgru = h1.hiscltr) where h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(
            folio) + " and h1.fhcindesp='TR'"


        cursor = con2.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Triage = []

        if rows == []:
            return localTriage
        else:
            for row in rows:
                localTriage=localTriage+1
                recibo = self.cabezote( doc, localTriage, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 , headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento)
                localTriage= recibo
                Story.append(Spacer(1, 5))
                texto1 = 'TRIAGE (MOTIVO DE CONSULTA)'
                localTriage = localTriage + 4
                recibo = self.cabezote(doc, localTriage, Story, tipodoc, documento, folio, headline_mayor,headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,subtitle_nacimiento)
                localTriage = recibo
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 4))
                Story.append(Paragraph('TRIAGE ' + str(row.TRIAGE), subtitle_atencion))
                Story.append(Spacer(1, 2))
                texto1 = 'OBSERVACIONES'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 2))
                Story.append(Paragraph(str(row.OBSERVACIONES), subtitle_atencion))
                Story.append(Spacer(1, 4))

                tbl_data = [
                    [Paragraph("CLASIFICACION TRIAGE: " ,headline_mayor3),
                     Paragraph(str(row.CLASIFICACION_TRIAGE) , subtitle_atencion),
                     Paragraph(str(row.TRIAGE_PRIORIDAD), subtitle_atencion),
                     Paragraph(" " , subtitle_atencion)]]

                tbl1 = Table(tbl_data, colWidths=[6 * cm, 4 * cm, 4 * cm, 7.3 * cm])
                Story.append(tbl1)
                #Story.append(Spacer(1, 2))
                localTriage=localTriage+7
                recibo = self.cabezote(doc, localTriage, Story, tipodoc, documento, folio, headline_mayor,     headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                       headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
                localTriage = recibo
        con2.close()
        localRegistro = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,    subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        return localTriage



    def registro(self,  doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Registro Medico
        localRegistro = y
        print("Entre Registro con y = ", y)


        con6 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  mae.mmnomm MEDICO, mae.mmregm as registro,esp.menome especialidad, mae.mmfirma as ruta_firma " \
                  "from hosvital.hccom1 h1 INNER JOIN HOSVITAL.MaEMED1 MAE on (mae.mmcodm = h1.hiscmmed) " \
                  "inner join hosvital.maeesp esp on (esp.mecode= h1.hcesp) where  h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(
            folio)


        cursor = con6.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()


        if rows == []:
            return localRegistro
        else:
            for row in rows:
                localRegistro = localRegistro + 1
                recibo = self.cabezote(doc, localRegistro, Story, tipodoc, documento, folio, headline_mayor,headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,  subtitle_nacimiento)
                localRegistro = recibo
                Story.append(Spacer(1, 40))

                if row.RUTA_FIRMA != ' ':
                    imagen1 = Image(row.RUTA_FIRMA, 1 * inch, 1 * inch)
                    Story.append(imagen1)
                #Story.append(Paragraph(imagen1, estilos1["Justify_left"]))
                texto1 = '_________________________'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 2))
                #imagen_logo = Image(os.path.realpath(row.RUTA_FIRMA), width=192, height=92)
                #print(imagen_logo)
                # Story.append(Paragraph(str(imagen_logo), estilos1["Justify_left"]))
                # Story.append(Spacer(1, 2))
                localRegistro = localRegistro + 1
                recibo = self.cabezote(doc, localRegistro, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1,
                                       headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                       subtitle_tipoevol,
                                       subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
                localRegistro = recibo

                Story.append(Paragraph(str(row.MEDICO), headline_mayor))
                Story.append(Spacer(1, 3))
                localRegistro = localRegistro + 3
                recibo = self.cabezote(doc, localRegistro, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1,
                                       headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                       subtitle_tipoevol,
                                       subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
                localRegistro = recibo
                Story.append(Paragraph('Reg. ' + str(row.REGISTRO), headline_mayor))
                Story.append(Spacer(1, 3))
                localRegistro = localRegistro + 3
                recibo = self.cabezote(doc, localRegistro, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1,
                                       headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                       subtitle_tipoevol,
                                       subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
                localRegistro = recibo
                Story.append(Paragraph(str(row.ESPECIALIDAD), headline_mayor))
                Story.append(Spacer(1, 4))
                localRegistro = localRegistro + 4
                recibo = self.cabezote(doc, localRegistro, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1,
                                       headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                       subtitle_tipoevol,
                                       subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
                localRegistro = recibo



        con6.close()
        return localRegistro

    def evoluciones(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):
        # Trae Evoluciones

        localEvoluciones = y
        print("Entre Evoluciones con y = ", y)


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
                  "where des1.histipdoc='" + tipodoc + "' and des1.hisckey='" + documento + "' and des1.hiscsec= " + str(folio) + " and h1.fhcindesp IN ('GN') union select h1.hiscsec as folio,h1.hisfhorat, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion, " \
                      "'EVOLUCION MEDICA' TIPO, H33.evodes as descripcion,   h1.hiscenfact as enfermedad_actual " \
                      "from   hosvital.hccom1 h1  left join hosvital.hccom33 h33 on (h33.histipdoc=h1.histipdoc and h33.hisckey=h1.hisckey and h33.hiscsec = h1.hiscsec) " \
                      "where h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec=" + str(folio) + " and h1.fhcindesp IN ('GN')"


        cursor = con3.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Evoluciones = []
        imprimioEnf='No'
        # ojo en plan y manejo imoprime Evolución realizada por: JUAN JOSE CALDERÓN SUTA-Fecha: 26/05/21 17:00:04

        if rows == []:
            return localEvoluciones
        else:
            for row in rows:


                if imprimioEnf == 'No' and row.ENFERMEDAD_ACTUAL != '':
                    imprimioEnf= 'Si'
                    texto = 'ENFERMEDAD ACTUAL'
                    Story.append(Paragraph(texto, headline_mayor))
                    Story.append(Spacer(1, 4))
                    Story.append(Paragraph(str(row.ENFERMEDAD_ACTUAL), subtitle_atencion))
                    Story.append(Spacer(1, 3))

                Story.append(Paragraph(str(row.TIPO), headline_mayor))
                Story.append(Spacer(1, 5))
                localEvoluciones = localEvoluciones + 5
                Story.append(Paragraph(str(row.DESCRIPCION  ), subtitle_atencion))

                if row.TIPO == 'PLAN Y MANEJO':
                    tbl_data = [
                        [Paragraph("Evolucion realizada por:", headline_mayor33),
                         Paragraph("Falta el nombre", headline_mayor33),
                         Paragraph("Fecha:", headline_mayor33), Paragraph(str(row.FECHA), headline_mayor33),
                         # Paragraph("", headline_mayor33),
                         ]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 7 * cm, 3 * cm, 5 * cm])

                    Story.append(tbl1)

                Story.append(Spacer(1, 6))
                localEvoluciones = localEvoluciones + 7
                recibo = self.cabezote(doc, localEvoluciones, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                       headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                       subtitle_nacimiento)
                localEvoluciones = recibo
        con3.close()

        return  localEvoluciones


    def diagnosticos(self,doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Diagnosticos
        localDiagnosticos = y
        print("Entre Diagnosticos con y = ", y)

        con4 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  hc.histipdoc,hc.hisckey,hc.hiscsec as folio, hc.hcdxcod cod_dx, m.dmnomb diagnostico  , case when hc.hcdxcls=2 then 'DESCARTADO'  when hc.hcdxcls=1 then 'PRINCIPAL' when hc.hcdxcls=0 then 'RELACIONADO'  END tipo " \
                  "from hosvital.hcdiagn hc inner join hosvital.maedia m on (m.dmcodi= hc.hcdxcod) " \
                  "where hc.histipdoc='" + tipodoc + "' and hc.hisckey = '" + documento + "' and hc.hiscsec = " + str(folio) + " order by hc.hcdxcls, hc.hccnsdx"


        cursor = con4.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()
        Diagnosticos = []

        Story.append(Spacer(1, 3))

        if rows ==   []:
            return localDiagnosticos
        else:
            for row in rows:
                localDiagnosticos = localDiagnosticos + 1
                recibo = self.cabezote(doc, localDiagnosticos, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                       headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                       subtitle_nacimiento)
                localDiagnosticos = recibo


                tbl_data1 = [
                    [Paragraph("DIAGNOSTICO:", headline_mayor),
                     Paragraph(str(row.COD_DX) , subtitle_atencion),
                     Paragraph(str(row.DIAGNOSTICO), subtitle_atencion),
                     Paragraph("Tipo", headline_mayor),
                     Paragraph(str(row.TIPO), subtitle_atencion),
                     ]]


                tbl1 = Table(tbl_data1)
                Story.append(tbl1)

                Story.append(Spacer(1, 3))

        localDiagnosticos = localDiagnosticos + 3
        recibo = self.cabezote(doc, localDiagnosticos, Story, tipodoc, documento, folio, headline_mayor,
                               headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                               headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                               subtitle_nacimiento)
        localDiagnosticos = recibo

        con4.close()

        return localDiagnosticos

    def formulacion(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Formulacion
        localFormulaciones = y
        print("Entre Formulaciones con y = ", y)

        con7 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  a.hiscsec as folio, h1.hisfhorat fecha,  a.fsmcntdia as cantidad, concat(concat(a.hiscansum , ' ')   , u.unmddes)     as Dosis, a.fsmdscmdc as descripcion,via.viapldsc as via, " \
                  "case when a.hcfsfrh = 99  then 'Infusion Continua'  when a.hcfsfrh = 95 then 'Ahora' when a.hcfsfrh = 93  then 'Dosis Unica'  when a.hcfsfrh = 24 then '24 Horas' when a.hcfsfrh = 12 then '12 Horas'  when a.hcfsfrh = 8 then '8 Horas' when a.hcfsfrh = 6 then '6 Horas' when a.hcfsfrh = 4 then '4 Horas'  when a.hcfsfrh = 91 then '1 Hora'  when a.hcfsfrh = 1 then '1 Hora'   else cast(a.hcfsfrh as varchar(10)) end  as frecuencia, " \
                  "case when a.hcsmstgr = 'O' then 'Nuevo'  when a.hcsmstgr = 'S' then 'Suspendido'   when a.hcsmstgr = 'M' then 'Modificado'   when a.hcsmstgr = 'C' then 'Continuar'   when a.hcsmstgr = 'D' then '' " \
                  "when a.hcsmstgr = 'N' then 'Sin Cambios'     when a.hcsmstgr = 'A' then ''   when a.hcsmstgr = 'N' then 'Nuevo' END ACCION " \
                  "from hosvital.FrmSmns as a inner join hosvital.undmedi u on (u.unmdcod=a.hcsmundcd) inner join hosvital.maeviapl via on (via.viaplcod=a.hcfsvia) " \
                  "inner join hosvital.hccom1 h1 on (h1.histipdoc = a.histipdoc and h1.hisckey=a.hisckey  and h1.hiscsec=a.hiscsec ) " \
                  "where  a.histipdoc='" + tipodoc + "' and a.hisckey='" + documento + "' and a.hiscsec= " + str(folio) + " and a.hcsmstgr <> 'X' order by a.hiscsec"


        cursor = con7.cursor()
        cursor.execute(comando)
        rowsFormula = cursor.fetchall()
        Formulacion = []

        if rowsFormula == []:
            print("No encontre Formulaciones")
            return localFormulaciones
        else:
            texto = 'FORMULA MEDICA'
            Story.append(Paragraph(texto, headline_mayor))
            Story.append(Spacer(1, 2))

            localFormulaciones = localFormulaciones + 3
            recibo = self.cabezote(doc, localFormulaciones, Story, tipodoc, documento, folio, headline_mayor,
                                   headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                   headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                   subtitle_nacimiento)
            localFormulaciones = recibo


            tbl_data = [
                [Paragraph("Cantidad:", headline_mayor1), Paragraph("Dosis:", headline_mayor1),
                 Paragraph("Descripcion:", headline_mayor1), Paragraph("via:", headline_mayor1),
                 Paragraph("Frecuencia:", headline_mayor1), Paragraph("Accion:", headline_mayor1),
                 #Paragraph("", subtitle_atencion),
                 ],
            ]

            tbl = Table(tbl_data, colWidths=[2 * cm, 3.5 * cm, 7.5 * cm, 3 * cm, 2.5 * cm, 2 * cm])


            Story.append(tbl)
            Story.append(Spacer(1, 2))
            localFormulaciones = localFormulaciones + 2

            for rowFormula in rowsFormula:
                localFormulaciones = localFormulaciones + 1
                recibo = self.cabezote(doc, localFormulaciones, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                       headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                       subtitle_nacimiento)
                localFormulaciones = recibo

                tbl_data = [
                    [
                     #Paragraph("",   subtitle_atencion),
                     Paragraph(str(rowFormula.CANTIDAD),   subtitle_atencion), Paragraph(str(rowFormula.DOSIS) ,subtitle_atencion),
                     Paragraph(str(rowFormula.DESCRIPCION), subtitle_atencion), Paragraph(str(rowFormula.VIA)   ,subtitle_atencion),
                     Paragraph(str(rowFormula.FRECUENCIA), subtitle_atencion), Paragraph(str(rowFormula.ACCION),subtitle_atencion),
                     #Paragraph("", subtitle_atencion),
                     ],
                ]

                tbl = Table(tbl_data, colWidths=[ 1.5 * cm, 3.5 * cm, 7.5 * cm, 3 * cm, 2 * cm, 2 * cm])

                Story.append(tbl)

        Story.append(Spacer(1, 4))
        localFormulaciones = localFormulaciones + 4

        recibo = self.cabezote(doc, localFormulaciones, Story, tipodoc, documento, folio, headline_mayor,
                               headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                               headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                               subtitle_nacimiento)
        localFormulaciones = recibo
        con7.close()

        return localFormulaciones



    def notasEnf(self,  doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Registro Medico
        localNotasEnf = y
        print("Entre Notas enfermeria con y = ", y)


        con8 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio, h1.hisfhorat as fecha_folio, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion, h33.evodes EVOLUCION, 'Nota realizada por:' NOTA1, maemed1.mmnomm  ENFERMERA, concat(concat(cast(h33.evofec as varchar(10)), ' '), h33.evohor) FECHA " \
        	      "from hosvital.hccom1 h1 left join hosvital.hccom33 h33 on (h33.histipdoc = h1.histipdoc and h33.hisckey = h1.hisckey and h33.hiscsec = h1.hiscsec) inner join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h33.evomed) " \
        	       "where h1.histipdoc = '" + tipodoc + "' and h1.hisckey = '" + documento + "' and h1.hiscsec = " + str(folio) + " and h1.fhcindesp IN ('EN')"


        cursorEnf = con8.cursor()
        cursorEnf.execute(comando)
        rowsEnf = cursorEnf.fetchall()


        if rowsEnf == []:
            return localNotasEnf
        else:
            for rowEnf in rowsEnf:
                localNotasEnf = localNotasEnf + 1

                recibo = self.cabezote(doc, localNotasEnf, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                       headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                       subtitle_nacimiento)
                localNotasEnf = recibo

                texto1 = 'NOTAS ENFERMERIA'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 4))
                Story.append(Paragraph(str(rowEnf.EVOLUCION), subtitle_atencion))

                tbl_data = [
                    [Paragraph("Nota realizada por:", headline_mayor33), Paragraph(str(rowEnf.ENFERMERA), headline_mayor33),
                     Paragraph("FECHA:", headline_mayor33), Paragraph(str(rowEnf.FECHA), headline_mayor33),
                     #Paragraph("", headline_mayor33),
                           ]]

                tbl1 = Table(tbl_data, colWidths=[4 * cm, 7 * cm, 3 * cm , 5 * cm])

                Story.append(tbl1)
                localNotasEnf = localNotasEnf + 1

        Story.append(Spacer(1, 1))
        localRegistro = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        Story.append(Spacer(1, 1))

        localNotasEnf = localNotasEnf + 5
        recibo = self.cabezote(doc, localNotasEnf, Story, tipodoc, documento, folio, headline_mayor,
                               headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                               headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                               subtitle_nacimiento)
        localNotasEnf = recibo
        con8.close()
        return localNotasEnf

    def laboratorios(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2,
                 headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,
                 subtitle_cabezote, subtitle_nacimiento):

        # Trae Registro Medico
        localLaboratorios = y
        print("Entre Laboratorios con y = ", y)

        con9 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio, h5.hcprccod, h1.hisfhorat as fecha_folio, h5.hiscpcan cantidad ,maepro.prnomb as descripcion,   h5.hiscpobs descripcion1,case when h5.hcprstgr='C' THEN 'Cancelado'   when h5.hcprstgr='N' THEN 'No se realizo' when h5.hcprstgr='E' THEN 'En Proceso' when h5.hcprstgr='A' THEN 'Realizado' when h5.hcprstgr='O' THEN 'Pendiente' when h5.hcprstgr='I' THEN 'Interpretado'  END as estado, " \
                  "r51.hcfechres as fecha_hora_aplicacion ,resul.reddesca  as resultados, concat(concat(resul.redresu,' '), resul.redunmer) valor, resul.redvalrf referencia,concat(maemed11.mmcedm ,maemed11.mmnomm ) as realizado_por, maemed1.mmnomm as interpretado_por, h51.hcfehint fecha_interpreta, h51.hcintres interpretacion " \
                  "from hosvital.hccom5 h5 inner join hosvital.hccom51 h51 on (h51.histipdoc=h5.histipdoc and h51.hisckey=h5.hisckey and h51.hiscsec= h5.hiscsec and h51.hcprccod = h5.hcprccod) " \
                  "inner join hosvital.hccom1 h1 on (h1.histipdoc=h5.histipdoc and h1.hisckey=h5.hisckey and h1.hiscsec= h5.hiscsec) " \
                  "inner join hosvital.maepro maepro on (maepro.prcodi= h5.hcprccod) left join hosvital.hccom51R  r51 on (r51.histipdoc=h5.histipdoc and r51.hisckey=h1.hisckey and r51.hiscsec= h5.hiscsec and r51.hcprccns =  h51.hcprccns and r51.hcprccod = h5.hcprccod and  r51.hcprccns = h51.hcprccns and " \
                  "r51.hcconres = (select max(r511.hcconres) from hosvital.hccom51r r511 where r511.histipdoc=h51.histipdoc and r511.hisckey = h51.hisckey and r511.hiscsec=h51.hiscsec and r511.hcprccod=h51.hcprccod and r511.hcprccns= h51.hcprccns)) " \
                  "left join  interlab.detresu resul on (  substring(resul.orclin,(locate(' ',resul.orclin) + 1),2) = h5.histipdoc and  substring(resul.orclin,1,(locate(' ',resul.orclin) -1))    =  h5.hisckey and substring(resul.orclin,  (locate(' ',resul.orclin) + 4), 11) = cast(h5.hiscsec as varchar(11))    and resul.ordcodex = h5.hcprccod) " \
                  "left   join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h51.hcmedint) left join hosvital.maemed1 maemed11 on (maemed11.mmusuario= h51.rprusrrgs and maemed11.mmcedm<> '0') " \
                  "wHere  h5.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(
            folio) + " and h5.hcprctip =  2 AND H51.HCPRCCNS = (select max(h511.hcprccns) from hosvital.hccom51 h511 where h511.histipdoc=h51.histipdoc and h511.hisckey = h51.hisckey and h511.hiscsec=h51.hiscsec and h511.hcprccod=h51.hcprccod) order by h5.hcprccod,resul.reddesca"

        cursorLab = con9.cursor()
        cursorLab.execute(comando)
        rowsLab = cursorLab.fetchall()

        if rowsLab == []:
            return localLaboratorios
        else:
            localLaboratorios = localLaboratorios + 1

            recibo = self.cabezote(doc, localLaboratorios, Story, tipodoc, documento, folio, headline_mayor,
                                   headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                   headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                   subtitle_nacimiento)
            localLaboratorios = recibo

            texto1 = 'ORDENES DE LABORATORIO'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("descripcion", subtitle_atencion)
                         ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 12 * cm])

            localLaboratorios = localLaboratorios + 3
            recibo = self.cabezote(doc, localLaboratorios, Story, tipodoc, documento, folio, headline_mayor,
                                   headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                   headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                   subtitle_nacimiento)
            localLaboratorios = recibo

            Story.append(tbl1)
            for rowLab in rowsLab:
                tbl_data = [
                    [Paragraph(str(rowLab.CANTIDAD) , subtitle_atencion),Paragraph(str(rowLab.DESCRIPCION), subtitle_atencion),
                     Paragraph(str(rowLab.ESTADO), subtitle_atencion),
                     #Paragraph("", headline_mayor33),
                     ]]
                localLaboratorios = localLaboratorios + 1
                recibo = self.cabezote(doc, localLaboratorios, Story, tipodoc, documento, folio, headline_mayor,
                                       headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                                       headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                       subtitle_nacimiento)
                localLaboratorios = recibo
                tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])

                Story.append(tbl1)

        Story.append(Spacer(1, 1))
        localRegistro = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                      headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        Story.append(Spacer(1, 1))

        localLaboratorios = localLaboratorios + 2
        recibo = self.cabezote(doc, localLaboratorios, Story, tipodoc, documento, folio, headline_mayor,
                               headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,
                               headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                               subtitle_nacimiento)
        localLaboratorios = recibo
        con9.close()
        return localLaboratorios

class inicioView(TemplateView):
    print("Entre Inicio")
    template_name = 'inicio4.html'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi Inicio'
        contratosHC = ContratosHc.objects.all()


        context['ContratosHC'] = contratosHC

        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST inicio")

        usuario = request.POST.get('usuario');
        contrasena = request.POST.get('contrasena');
        seleccion = request.POST.get('seleccion');
        print(usuario)
        print(contrasena)

        print(seleccion)

        #  Arrancamos
        mensaje=""
        usuarioHC = UsuariosHc.objects.all().filter(usuario=usuario).filter(contrasena=contrasena)
        contratoHC = UsusariosContratosHc.objects.all().filter(usuario=usuario).filter(mpmeni=seleccion)

        print(usuarioHC)
        context = {}

        if usuarioHC:
            print("Si lo encontro")
            mensaje = ""

            if contratoHC:
                context['Mensaje'] = mensaje
                return render(request, "mitemplate2.html", context)
            else:
                mensaje = "Contrato No autorizado para el usuario ! "
                context['Mensaje'] = mensaje
                contratosHC = ContratosHc.objects.all()

                context['ContratosHC'] = contratosHC
                return render(request, "inicio4.html", context)


        else:
            print("No lo encontro")
            mensaje = "Usuario No Encontrado y/o Contraseña Invalida ! "
            context['Mensaje'] = mensaje
            contratosHC = ContratosHc.objects.all()


            context['ContratosHC'] = contratosHC

            return render(request, "inicio4.html", context)

def grabar(request, usuario, contrasena):
        print("Entre a grabar")
        usuario = request.POST["usuario"]

        contrasena = request.POST["contrasena"]

        print(usuario)

        print(contrasena)
        data1 = {}
        usuarioHC = UsuariosHc.objects.all().filter(usuario=usuario)
        if usuarioHC:
            usuarioHC1 = UsuariosHc.objects.get(usuario=usuario)
            usuarioHC1.contrasena = contrasena
            usuarioHC1.save()
            #data1={'Error',"ok"}
            return HttpResponse("ok")
        else:
            #data1 = {'Error', "Usuario No existe ! "}
            return HttpResponse("Usuario No existe ! ")


class AdmUsuariosView(TemplateView):
    print("Entre Inicio5")
    template_name = 'inicio5.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi Inicio'
        usuariosHc = UsuariosHc.objects.all()

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
        usuariosHc = UsuariosHc.objects.all()

        context['UsuariosHc'] = usuariosHc

        return render(request, "inicio5.html", context)

def Modal(request, usuario, contrasena, nombre):
        print("Entre a Modal")
        usuario = request.POST["usuario"]
        contrasena = request.POST["contrasena"]
        print(usuario)
        print(contrasena)

        UsuariosHC = UsuariosHc.objects.get(usuario=usuario)
        return JsonResponse(UsuariosHC)


def grabar1(request, usuario, contrasena,nombre):
    print("Entre a grabar1")
    usuario = request.POST["usuario"]

    contrasena = request.POST["contrasena"]
    nombre = request.POST["nombre"]

    print(usuario)

    print(contrasena)
    print(nombre)
    data1 = {}
    usuarioHC = UsuariosHc.objects.all().filter(usuario=usuario)
    if usuarioHC:
        usuarioHC1 = UsuariosHc.objects.get(usuario=usuario)
        usuarioHC1.contrasena = contrasena
        usuarioHC1.nombre = nombre
        usuarioHC1.save()
        # data1={'Error',"ok"}
        return HttpResponse("ok")
    else:
        # data1 = {'Error', "Usuario No existe ! "}
        return HttpResponse("Usuario No existe ! ")

from django.shortcuts import render
import csv
from django.views.generic import ListView, CreateView, TemplateView, View
from django.shortcuts import render
from django.http import HttpResponse
from reporte01.forms import VistaCexForm  # El formulario que creaste
from reporte01.models import VistaCex
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
from datetime import datetime
from datetime import date
from reportlab.lib.fonts import addMapping
from reportlab.lib.colors import (
black,
purple,
white,
yellow
)

tipodoc = "CC"
documento = ""
Story = []



# Create your views here.
class nuevoPdfView(TemplateView):
    print("pdf1")
    template_name = 'mitemplate2.html'
    y=0
    tipodoc = "CC"
    documento = "5812348"

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



    def myFirstPage(self,canvas, doc):
        print("Entre MyFirstPag")
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)
        global tipodoc
        global documento
        print(documento)
        print(tipodoc)


        #  INSERTO CODIGO DESDE CABEZOTE
        logotipo = "C:\\EntornosPython\\reportes\\reportes\\static\\images\\logo.jpg"
        imagen = Image(logotipo, 0.6 * inch, 0.6 * inch)
        imagen.hAlign = 'LEFT'

        fecha = date.today()
        format = fecha.strftime('%d / %m / %Y')
        print(format)
        print(fecha)
        canvas.drawImage("C:\\EntornosPython\\reportes\\reportes\\static\\images\\logo.jpg", 40, 715, width=50,
                         height=50)
        canvas.drawString(220, 750, "FUNDACION HOSPITAL SAN CARLOS")
        canvas.drawString(275, 735, "860007373 - 4")
        canvas.drawString(340, 715, "Fecha:")
        canvas.drawString(400, 715, str(format))
        canvas.drawString(500, 715, "Pág: %d " % (doc.page))
        #canvas.drawString(520, 715, "de %d " % (doc.pageCount))
        # canvas.drawString(380, 715, fecha)

        # Trae el cabezote

        con1 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select cap.mptdoc tipodoc, cap.mpcedu documento, cap.mpnomc paciente, maeemp.menomb as empresa ,   maetpa3.mtnomp as afiliado, varchar_format(cap.mpfchn ,'dd/mm/yyyy') as fecha_nacimiento , concat((days(current_date) - days(date(cap.mpfchn)))/365, ' AÑOS') as edad_actual, case when cap.mpsexo='M' then 'Masculino'  when cap.mpsexo='F' then 'Femenino' end  as sexo, cap.MPTipAfi	  as grupo_sanguineo,    case when cap.MPEstC= 'C' THEN 'Casado'      when cap.MPEstC= 'S' THEN 'Soltero'  when cap.MPEstC= 'U' THEN 'Union Libre'  when cap.MPEstC= 'V' THEN 'Viudo'  when cap.MPEstC= 'P' THEN 'Separado'  when cap.MPEstC= 'O' THEN ''        ELSE ''        end          as estado_civil,     cap.mptele as telefono,cap.mpdire as direccion,   " \
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

        if rows == []:
            print("Paciente No existe")
            canvas.restoreState()
            return 0

        for row in rows:
            texto = 'HISTORIA CLINICA No '

            canvas.drawString(40, 690, texto)
            canvas.drawString(150, 690, tipodoc)
            canvas.drawString(165, 690, documento)
            canvas.drawString(220, 690, row.PACIENTE)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 660, "Empresa:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 660, row.EMPRESA)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 660, "Afiliado:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 660, row.AFILIADO)
            canvas.setFont('Helvetica-Bold', 9)

            canvas.drawString(40, 650, "Fecha Nacimiento:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(125, 650, row.FECHA_NACIMIENTO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(170, 650, "Edad Actual:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(230, 650, row.EDAD_ACTUAL)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(270, 650, "Sexo:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(300, 650, row.SEXO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 650, "Grupo Sanguineo:")
            canvas.setFont('Times-Roman', 9)
            # canvas.drawString(160,655, row.GRUPO_SANGUINEO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(450, 650, "Estado Civil:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(520, 650, row.ESTADO_CIVIL)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 640, "Telefono:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 640, row.TELEFONO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 640, "Direccion:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 640, row.DIRECCION)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 630, "Barrio:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 630, row.BARRIO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 630, "Departamento:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 630, row.DEPARTAMENTO)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 620, "Municipio:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 620, row.MUNICIPIO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 620, "Ocupacion:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 620, row.OCUPACION)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 610, "Etnia:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 610, row.ETNIA)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 610, "Grupo Etnico:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 610, row.GRUPO_ETNICO)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 600, "Nivel Educativo:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 600, row.NIVEL_EDUCATIVO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 600, "Atencion Especial:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 600, row.NIVEL_EDUCATIVO)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 590, "Discapacidad:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 590, row.DISCAPACIDAD)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 590, "Grupo Poblacional:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 590, row.GRUPO_POBLACIONAL)
            texto1 = '_________________________________________________________________________________________________________'
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 580, texto1)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 570, "Responsable:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 570, row.RESPONSABLE)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 570, "Telefono:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 570, row.TELEFONORESP)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 560, "Acompañante:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 560, row.ACOMPANANTE)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 560, "Telefono:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 560, row.TELEFONO_ACOMPANANTE)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 550, texto1)

        con1.close()

        ### FIN INSERTO CABEZOTE

        pageinfo = "Ejemplo Platypus"
        #canvas.drawString(inch, 0.75 * inch, "Página %d " % (doc.page))
        canvas.restoreState()

    # Definimos disposiciones alternas para las caracteristicas de las otras páginas

    def myLaterPages(self,canvas, doc):
        print("Entre myLaterPages")
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)
        global tipodoc
        global documento
        print(documento)
        print(tipodoc)


        #  INSERTO CODIGO DESDE CABEZOTE
        logotipo = "C:\\EntornosPython\\reportes\\reportes\\static\\images\\logo.jpg"
        imagen = Image(logotipo, 0.6 * inch, 0.6 * inch)
        imagen.hAlign = 'LEFT'

        fecha = date.today()
        format = fecha.strftime('%d / %m / %Y')
        print(format)
        print(fecha)
        canvas.drawImage("C:\\EntornosPython\\reportes\\reportes\\static\\images\\logo.jpg", 40, 715, width=50,
                         height=50)
        canvas.drawString(220, 750, "FUNDACION HOSPITAL SAN CARLOS")
        canvas.drawString(275, 735, "860007373 - 4")
        canvas.drawString(340, 715, "Fecha:")
        canvas.drawString(400, 715, str(format))
        canvas.drawString(500, 715, "Pág: %d " % (doc.page))
        #canvas.drawString(520, 715, "de %d " % (doc.pageCount))
        # canvas.drawString(380, 715, fecha)

        # Trae el cabezote

        con1 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select cap.mptdoc tipodoc, cap.mpcedu documento, cap.mpnomc paciente, maeemp.menomb as empresa ,   maetpa3.mtnomp as afiliado, varchar_format(cap.mpfchn ,'dd/mm/yyyy') as fecha_nacimiento , concat((days(current_date) - days(date(cap.mpfchn)))/365, ' AÑOS') as edad_actual, case when cap.mpsexo='M' then 'Masculino'  when cap.mpsexo='F' then 'Femenino' end  as sexo, cap.MPTipAfi	  as grupo_sanguineo,    case when cap.MPEstC= 'C' THEN 'Casado'      when cap.MPEstC= 'S' THEN 'Soltero'  when cap.MPEstC= 'U' THEN 'Union Libre'  when cap.MPEstC= 'V' THEN 'Viudo'  when cap.MPEstC= 'P' THEN ''  when cap.MPEstC= 'O' THEN ''        ELSE ''        end          as estado_civil,     cap.mptele as telefono,cap.mpdire as direccion,   " \
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

        if rows == []:
            print("Paciente No existe")
            return 0

        for row in rows:
            texto = 'HISTORIA CLINICA No '

            canvas.drawString(40, 690, texto)
            canvas.drawString(150, 690, tipodoc)
            canvas.drawString(165, 690, documento)
            canvas.drawString(220, 690, row.PACIENTE)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 660, "Empresa:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 660, row.EMPRESA)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 660, "Afiliado:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 660, row.AFILIADO)
            canvas.setFont('Helvetica-Bold', 9)

            canvas.drawString(40, 650, "Fecha Nacimiento:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(125, 650, row.FECHA_NACIMIENTO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(170, 650, "Edad Actual:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(230, 650, row.EDAD_ACTUAL)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(270, 650, "Sexo:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(300, 650, row.SEXO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 650, "Grupo Sanguineo:")
            canvas.setFont('Times-Roman', 9)
            # canvas.drawString(160,655, row.GRUPO_SANGUINEO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(450, 650, "Estado Civil:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(520, 650, row.ESTADO_CIVIL)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 640, "Telefono:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 640, row.TELEFONO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 640, "Direccion:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 640, row.DIRECCION)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 630, "Barrio:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 630, row.BARRIO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 630, "Departamento:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 630, row.DEPARTAMENTO)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 620, "Municipio:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 620, row.MUNICIPIO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 620, "Ocupacion:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 620, row.OCUPACION)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 610, "Etnia:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 610, row.ETNIA)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 610, "Grupo Etnico:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 610, row.GRUPO_ETNICO)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 600, "Nivel Educativo:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 600, row.NIVEL_EDUCATIVO)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 600, "Atencion Especial:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 600, row.NIVEL_EDUCATIVO)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 590, "Discapacidad:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 590, row.DISCAPACIDAD)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 590, "Grupo Poblacional:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 590, row.GRUPO_POBLACIONAL)
            texto1 = '_________________________________________________________________________________________________________'
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 580, texto1)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 570, "Responsable:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 570, row.RESPONSABLE)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 570, "Telefono:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 570, row.TELEFONORESP)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 560, "Acompañante:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(120, 560, row.ACOMPANANTE)
            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(340, 560, "Telefono:")
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(430, 560, row.TELEFONO_ACOMPANANTE)

            canvas.setFont('Helvetica-Bold', 9)
            canvas.drawString(40, 550, texto1)

        con1.close()

        ### FIN INSERTO CABEZOTE

        pageinfo = "Ejemplo Platypus"
        #canvas.drawString(inch, 0.75 * inch, "Página %d " % (doc.page))
        canvas.restoreState()


    def cabezote(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,  subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento,lineas):

            localcabezote = y
            print("Entre Cabezote Folio , Linea  " , folio,  y)
            return localcabezote

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'
        print("POR QUI PASE")
        con001 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        cursor001 = con001.cursor()
        cursor001.execute(
            "SELECT  mptdoc mptdoc, mptdesc mptdesc FROM HOSVITAL.TIPDOCASI order by mptdesc")
        rows001 = cursor001.fetchall()
        TiposDoc  = []

        for row001 in rows001:
             TiposDoc.append({'MPTDOC': row001.MPTDOC, 'MPTDESC': row001.MPTDESC})
        print(TiposDoc )
        con001.close()

        context['TiposDoc'] = TiposDoc
        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST")
        global documento
        documento = request.POST.get('documento');
        global tipodoc
        tipodoc = request.POST.get('seleccion');

        Desde = request.POST.get('Desde', False);
        Hasta = request.POST.get('Hasta', False);

        resultado = buscapaciente(tipodoc,documento)

        if resultado != 0:
            mensaje = ""
            mensaje1 = {"mensaje": mensaje}
            context1 = {}
            context1['mensaje'] = mensaje1



        if resultado== 0:
            con002 = pyodbc.connect(
                'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

            cursor002 = con002.cursor()
            cursor002.execute(
                "SELECT  mptdoc mptdoc, mptdesc mptdesc FROM HOSVITAL.TIPDOCASI order by mptdesc")
            rows002 = cursor002.fetchall()
            TiposDoc = []

            for row002 in rows002:
                TiposDoc.append({'MPTDOC': row002.MPTDOC, 'MPTDESC': row002.MPTDESC})
            print(TiposDoc)
            con002.close()

            mensaje = "Paciente No existe. Favor verificar"
            mensaje1 = {"mensaje": mensaje}
            context1 = {}
            context1['TiposDoc'] = TiposDoc
            context1['mensaje'] = mensaje1

            return render(request, "mitemplate2.html", context1)

        Desde = Desde + " 00:00:00"
        Hasta = Hasta + " 23:59:59"


        #  Arrancamos

        # Story = []
        global Story
        #Story = [Spacer(0, 20)]
        buff = io.BytesIO()
        #doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=26,   leftMargin=32, topMargin=72, bottomMargin=18)
        doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=26, leftMargin=32, topMargin=240, bottomMargin=18)

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

        #subtitle_atencion = estilos["Heading3"]
        #subtitle_atencion.leading =9
        #subtitle_atencion.fontSize = 8
        #subtitle_atencion.fontName = "Times-Roman"
        #subtitle_atencion.spaceAfter = 0
        #subtitle_atencion.spaceBefore = 0
        #subtitle_atencion.alignment = TA_LEFT

        subtitle_atencion = estilos["Heading3"]
        subtitle_atencion.leading =9
        subtitle_atencion.fontSize = 8
        subtitle_atencion.fontName = "courier-bold"
        subtitle_atencion.spaceAfter = 0
        subtitle_atencion.spaceBefore = 0
        subtitle_atencion.alignment = TA_LEFT
        #Tahoma ,, courier

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

        estilos.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
        estilos1 = getSampleStyleSheet()
        estilos1.add(ParagraphStyle(name='Justify_left', alignment=TA_LEFT))
        estilos2 = getSampleStyleSheet()
        estilos2.add(ParagraphStyle(name='Justify_right', alignment=TA_RIGHT))
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="Historia.pdf"'
        response['Content-Disposition'] = 'attachment; filename="' + tipodoc + ' ' + documento + '.pdf"'

        con0 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')
        cursort = con0.cursor()

        comando = "select h1.hiscsec as folio, h1.hisfhorat as fecha_folio, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' when h1.hisclpr='5' then 'TRIAGE' end tipo_atencion , " \
                   "'FUNDACION HOSPITAL SAN CARLOS' empresa,(days(h1.hisfhorat) - days(date(cap.mpfchn)))/365 edadactual " \
                  "from hosvital.hccom1 h1 INNER JOIN HOSVITAL.CAPBAS CAP ON (CAP.MPTDOC = h1.histipdoc and CAP.MPCEDU = h1.HISCKEY) where h1.histipdoc='" + tipodoc + "' and h1.hisckey= '" + documento + "' and   " \
                  "h1.hisfhorat >= '" + Desde + "' and h1.hisfhorat <= '" + Hasta + "' and h1.fhcindesp not IN ('EN')  " \
                  "UNION select h1.hiscsec as folio, h1.hisfhorat as fecha_folio, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion , " \
                  "'FUNDACION HOSPITAL SAN CARLOS' empresa,(days(current_date) - days(date(cap.mpfchn)))/365 edadactual   "  \
                  "from hosvital.hccom1 h1 left join  hosvital.hccom33 h33 on (h33.histipdoc=h1.histipdoc and h33.hisckey=h1.hisckey and h33.hiscsec = h1.hiscsec ) left join hosvital.maemed1 maemed1 on (maemed1.mmcodm=h33.evomed)  INNER JOIN HOSVITAL.CAPBAS CAP ON (CAP.MPTDOC=h1.HISTIPDOC AND CAP.MPCEDU = h1.HISCKEY)  where h1.histipdoc='" + tipodoc +"' and h1.hisckey= '"  + documento + "' and h1.hisfhorat >= '" + Desde + "' and  h1.hisfhorat <= '" + Hasta + "' and h1.fhcindesp IN ('EN') order by 1"


        cursort.execute(comando)
        rowsGlobal = cursort.fetchall()

        y = 0
        lineas=0
        #localppal = self.cabezote(doc, y, Story, tipodoc, documento, 0,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento,lineas)

        mensaje = "Paciente No existe. Favor verificar"
        mensaje1 = {"mensaje":mensaje}
        localppal=200
        if localppal==0:
            con002 = pyodbc.connect(
                'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

            cursor002 = con002.cursor()
            cursor002.execute(
                "SELECT  mptdoc mptdoc, mptdesc mptdesc FROM HOSVITAL.TIPDOCASI order by mptdesc")
            rows002 = cursor002.fetchall()
            TiposDoc = []

            for row002 in rows002:
                TiposDoc.append({'MPTDOC': row002.MPTDOC, 'MPTDESC': row002.MPTDESC})
            print(TiposDoc)
            con002.close()

            context={}
            context['TiposDoc'] = TiposDoc
            context['mensaje'] = mensaje1

            return render(request, "mitemplate2.html", context)

        comienzaFolio = localppal

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

            tbl = Table(tbl_data1, colWidths=[5 * cm, 2 * cm, 8 * cm, 3 * cm, 2 * cm, 0.8 * cm])
            Story.append(tbl)
            texto1 = '______________________________________________________________________________________________________________'

            Story.append(Paragraph(texto1, subtitle_atencion))

            tbl_data = [
                [Paragraph("FOLIO:", headline_mayor33), Paragraph(str(rowGlobal.FOLIO), headline_mayor33),
                 Paragraph("FECHA:", headline_mayor33),Paragraph(str(rowGlobal.FECHA_FOLIO), headline_mayor33),
                 Paragraph("TIPO DE ATENCION:", headline_mayor33),Paragraph(str(rowGlobal.TIPO_ATENCION), headline_mayor33),
                 Paragraph("", headline_mayor33)],
            ]

            tbl1 = Table(tbl_data, colWidths=[1.5 * cm, 1.5 * cm, 2 * cm, 3.5 * cm, 6 * cm , 3.5 * cm, 1.5 * cm])

            Story.append(tbl1)

            texto1 = '______________________________________________________________________________________________________________'
            Story.append(Paragraph(texto1, subtitle_atencion))

            Story.append(Spacer(1, 1))

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
            localimagenes = self.imagenes(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                          headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                          subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
            y = localimagenes
            localprocNoQx = self.procNoQx(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                          headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                          subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
            y = localprocNoQx
            locallaboratorios = self.laboratorios(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,   headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
            y = locallaboratorios
            localQxCan       = self.QxCancela(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,        headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
            y = localQxCan
            localprocQx = self.procQx(doc, y, Story, tipodoc, documento, folio, headline_mayor,headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,  headline_mayor4, subtitle_tipoevol, subtitle_atencion,       subtitle_cabezote, subtitle_nacimiento)
            y = localprocQx

            localTerapiasCan = self.terapiasCancela(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
            y = localTerapiasCan

            localTerapias = self.terapias(doc, y, Story, tipodoc, documento, folio, headline_mayor,headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33,  headline_mayor4, subtitle_tipoevol, subtitle_atencion,        subtitle_cabezote, subtitle_nacimiento)
            y = localTerapias
            localTerapiasGases = self.terapiasGases(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                          headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                          subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
            y = localTerapiasGases
            localInterconsultas = self.interconsultas(doc, y, Story, tipodoc, documento, folio, headline_mayor,
                                                    headline_mayor1,
                                                    headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                                    subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                                    subtitle_nacimiento)
            y = localInterconsultas
            localIncapacidades = self.incapacidades(doc, y, Story, tipodoc, documento, folio, headline_mayor,headline_mayor1,headline_mayor2, headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                                      subtitle_nacimiento)
            y = localIncapacidades



            localCirugias = self.cirugias(doc, y, Story, tipodoc, documento, folio, headline_mayor,
                                                      headline_mayor1,
                                                      headline_mayor2, headline_mayor3, headline_mayor33,
                                                      headline_mayor4,
                                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                                      subtitle_nacimiento)
            y = localCirugias
            Story.append(Spacer(1, 3))

            localRegistro = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,  subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)

            comienzaFolio = localRegistro

        con0.close()
        #doc.build(Story)
        doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
        response.write(buff.getvalue())
        buff.close()
        return response

    def triage(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Triage

        localTriage = y
        print("Entre Triage con localTriage  folio y = ", localTriage, folio, y)

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


        if rows == []:
            return localTriage
        else:
            for row in rows:

                Story.append(Spacer(1, 5))
                texto1 = 'TRIAGE (MOTIVO DE CONSULTA)'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 4))
                Story.append(Paragraph('TRIAGE ' + str(row.TRIAGE), subtitle_atencion))
                lineas = 2
                localTriage = self.cabezote(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                            headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                            subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                            subtitle_nacimiento, lineas)
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

        con2.close()
        y=localTriage
        localTriage = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,    subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        return localTriage



    def registro(self,  doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Registro Medico
        localRegistro = y

        print("Entre Registro con localRegistro  folio y = ", localRegistro, folio, y)

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
                Story.append(Spacer(1,15))

                if row.RUTA_FIRMA != ' ':

                    if os.path.isfile(row.RUTA_FIRMA) == True:
                         imagen1 = Image(row.RUTA_FIRMA, 4 * cm, 1 * cm)
                         imagen1.hAlign = 'LEFT'
                         Story.append(imagen1)
                #Story.append(Paragraph(imagen1, estilos1["Justify_left"]))

                texto1 = '_____________________________________________'
                Story.append(Paragraph(texto1, subtitle_atencion))
                # Aqui el cambuio ESTABA EN 4
                Story.append(Spacer(1, 4))
                #imagen_logo = Image(os.path.realpath(row.RUTA_FIRMA), width=192, height=92)
                #print(imagen_logo)
                # Story.append(Paragraph(str(imagen_logo), estilos1["Justify_left"]))
                # Story.append(Spacer(1, 2))

                Story.append(Paragraph(str(row.MEDICO), headline_mayor))

                Story.append(Spacer(1, 3))
                Story.append(Paragraph('Reg. ' + str(row.REGISTRO), headline_mayor))
                Story.append(Spacer(1, 3))
                Story.append(Paragraph(str(row.ESPECIALIDAD), headline_mayor))
                lineas = 1
                localRegistro = self.cabezote(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                              headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                              subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                              subtitle_nacimiento, lineas)

                Story.append(Spacer(1, 2))


        con6.close()
        return localRegistro

    def evoluciones(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):
        # Trae Evoluciones

        localEvoluciones = y
        print("Entre Evoluciones con localEvoluciones  folio y = ", localEvoluciones, folio, y)

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
                  "when des1.hisdesatr='HISCREVS14' then 'REVISION 14' when des1.hisdesatr='HISCREVSI15' then 'REVISION 15'  END TIPO, des1.hisdesdet as descripcion,   h1.hiscenfact as enfermedad_actual , maemed1.mmnomm as medico " \
                  "from  hosvital.hccom1des des1 left join hosvital.hccom1 h1 on (h1.histipdoc=des1.histipdoc and h1.hisckey=des1.hisckey and h1.hiscsec = des1.hiscsec) left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h1.hiscmmed) " \
                  "where des1.histipdoc='" + tipodoc + "' and des1.hisckey='" + documento + "' and des1.hiscsec= " + str(folio) + " and h1.fhcindesp IN ('GN') union select h1.hiscsec as folio,h1.hisfhorat, case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion, " \
                      "'EVOLUCION MEDICA' TIPO, H33.evodes as descripcion,   h1.hiscenfact as enfermedad_actual , maemed1.mmnomm as medico " \
                      "from   hosvital.hccom1 h1  left join hosvital.hccom33 h33 on (h33.histipdoc=h1.histipdoc and h33.hisckey=h1.hisckey and h33.hiscsec = h1.hiscsec) left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h1.hiscmmed) " \
                      "where h1.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec=" + str(folio) + " and h1.fhcindesp IN ('GN')"


        cursor = con3.cursor()
        cursor.execute(comando)
        rows = cursor.fetchall()

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

                    Story.append(Paragraph(str(row.ENFERMEDAD_ACTUAL).replace("\n", "<br />"), subtitle_atencion))
                    Story.append(Spacer(1, 4))
                Story.append(Paragraph(str(row.TIPO).replace("\n", "<br />"), headline_mayor))

                Story.append(Spacer(1, 5))
                lineas = int(len(str(row.DESCRIPCION)) / 140) + int(str(row.DESCRIPCION).count("\n"))

                if lineas != 0:
                    Story.append(Paragraph(str(row.DESCRIPCION).replace("\n", "<br />"), subtitle_atencion))

                if row.TIPO == 'PLAN Y MANEJO':
                    tbl_data = [
                        [Paragraph("Evolucion realizada por:", headline_mayor33),
                         Paragraph(str(row.MEDICO), headline_mayor33),
                         Paragraph("Fecha:", headline_mayor33), Paragraph(str(row.FECHA), headline_mayor33),
                         # Paragraph("", headline_mayor33),
                         ]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 7 * cm, 3 * cm, 5 * cm])
                    Story.append(tbl1)

                Story.append(Spacer(1, 6))

        con3.close()

        return  localEvoluciones


    def diagnosticos(self,doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Diagnosticos
        localDiagnosticos = y
        print("Entre Diagnosticos con localDiagnosticos  folio y = ", localDiagnosticos, folio, y)

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



                tbl_data1 = [
                    [Paragraph("DIAGNOSTICO:", headline_mayor),
                     Paragraph(str(row.COD_DX) , subtitle_atencion),
                     Paragraph(str(row.DIAGNOSTICO), subtitle_atencion),
                     Paragraph("Tipo", headline_mayor),
                     Paragraph(str(row.TIPO), subtitle_atencion),
                     Paragraph(" ", subtitle_atencion),
                     ]]

                tbl1 = Table(tbl_data1, colWidths=[3.5 * cm, 2 * cm, 8 * cm, 2 * cm, 3 * cm, 0.5 * cm])


                Story.append(tbl1)

                Story.append(Spacer(1, 4))

        localDiagnosticos = localDiagnosticos + 3


        con4.close()

        return localDiagnosticos

    def formulacion(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33,headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Formulacion
        localFormulaciones = y
        print("Entre Formulacion con localFormulaciones  folio y = ", localFormulaciones, folio, y)

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



            tbl_data = [
                [Paragraph("Cantidad:", headline_mayor1), Paragraph("Dosis:", headline_mayor1),
                 Paragraph("Descripcion:", headline_mayor1), Paragraph("via:", headline_mayor1),
                 Paragraph("Frecuencia:", headline_mayor1), Paragraph("Accion:", headline_mayor1),
                 #Paragraph("", subtitle_atencion),
                 ],
            ]

            tbl = Table(tbl_data, colWidths=[2 * cm, 3 * cm, 7.5 * cm, 2.5 * cm, 2.5 * cm, 2 * cm])

            Story.append(tbl)
            Story.append(Spacer(1, 2))
            localFormulaciones = localFormulaciones + 2

            for rowFormula in rowsFormula:
                localFormulaciones = localFormulaciones + 1


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

        con7.close()

        return localFormulaciones



    def notasEnf(self,  doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Registro Medico
        localNotasEnf = y
        print("Entre Notas Enfermeria con localNotasEnf  folio y = ", localNotasEnf, folio, y)

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

                texto1 = 'NOTAS ENFERMERIA'
                lineas = 1
                localNotasEnf = self.cabezote(doc, y, Story, tipodoc, documento, folio, headline_mayor,
                                                 headline_mayor1,
                                                 headline_mayor2, headline_mayor3, headline_mayor33,
                                                 headline_mayor4,
                                                 subtitle_tipoevol, subtitle_atencion, subtitle_cabezote,
                                                 subtitle_nacimiento, lineas)

                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 4))
                Story.append(Paragraph(str(rowEnf.EVOLUCION).replace("\n", "<br />"), subtitle_atencion))

                tbl_data = [
                    [Paragraph("Nota realizada por:", headline_mayor33), Paragraph(str(rowEnf.ENFERMERA), headline_mayor33),
                     Paragraph("FECHA:", headline_mayor33), Paragraph(str(rowEnf.FECHA), headline_mayor33),
                     #Paragraph("", headline_mayor33),
                           ]]

                tbl1 = Table(tbl_data, colWidths=[4 * cm, 7 * cm, 3 * cm , 5 * cm])
                Story.append(tbl1)



        Story.append(Spacer(1, 1))
        #localNotasEnf = self.registro(doc, localNotasEnf, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)


        con8.close()
        return localNotasEnf

    def laboratorios(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2,
                 headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,
                 subtitle_cabezote, subtitle_nacimiento):

        # Trae Registro Medico
        localLaboratorios = y
        print("Entre Laboratorios con localLaboratorios  folio y = ", localLaboratorios, folio, y)


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


            texto1 = 'ORDENES DE LABORATORIO'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 2))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("descripcion", subtitle_atencion)
                         ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 12 * cm])

            localLaboratorios = localLaboratorios + 3


            Story.append(tbl1)
            lab =''
            lab1=''
            resul=''
            resul1=''
            for rowLab in rowsLab:
                lab1 = str(rowLab.DESCRIPCION)
                resul1=str(rowLab.RESULTADOS)


                if lab =='' or lab1 != lab:

                    tbl_data = [
                        [Paragraph(str(rowLab.CANTIDAD) , subtitle_atencion),Paragraph(str(rowLab.DESCRIPCION), subtitle_atencion),
                        Paragraph(str(rowLab.ESTADO), subtitle_atencion),
                        #Paragraph("", headline_mayor33),
                        ]]
                    localLaboratorios = localLaboratorios + 1

                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)
                    Story.append(Paragraph('Fecha y hora de Aplicacion: ' + str(rowLab.FECHA_HORA_APLICACION),                                      subtitle_atencion))
                    Story.append(Paragraph('Resultados: ', subtitle_atencion))

                    lab=lab1

                if resul == '' or resul1 != resul:

                    Story.append(Paragraph(str(rowLab.RESULTADOS).replace("\n", "<br />") + str(rowLab.VALOR).replace("\n", "<br />") + str(rowLab.REFERENCIA).replace("\n", "<br />") , subtitle_atencion))

                    resul = resul1
                else:
                    # if rowLab.REALIZADO_POR != '':
                    Story.append(Paragraph('Realizado Por: ' + str(rowLab.REALIZADO_POR), subtitle_atencion))

                    if rowLab.INTERPRETADO_POR != '':
                        Story.append(Paragraph('INTERPRETACION: ', subtitle_atencion))
                        Story.append(Spacer(1, 3))
                        Story.append(Paragraph(
                            'Interpretado por: ' + str(rowLab.INTERPRETADO_POR) + str(rowLab.FECHA_INTERPRETA),
                            subtitle_atencion))
                        Story.append(Paragraph(str(rowLab.INTERPRETACION), subtitle_atencion))



        Story.append(Spacer(1, 1))
        localRegistro = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                      headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        Story.append(Spacer(1, 1))

        localLaboratorios = localLaboratorios + 2
        con9.close()
        return localLaboratorios



    def imagenes(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Triage
        localImagen = y
        print("Entre Imagenes con localImagen  folio y = ", localImagen, folio, y)



        localImagen = self.cabezote(doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 , headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento,0)

        con10 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio,h5.hcprccod , r51.hcprccns  ,  h1.hisfhorat as fecha_folio,h5.hiscpcan cantidad , maepro.prnomb as descripcion,case when h5.hcprstgr='C' THEN 'Cancelado'   when h5.hcprstgr='N' THEN 'No se realizo'   when h5.hcprstgr='E' THEN 'En Proceso'  when  h5.hcprstgr='A' THEN 'Realizado'  when h5.hcprstgr='O' THEN 'Pendiente' when h5.hcprstgr='I' THEN 'Interpretado'  END estado, " \
                  "h5.hiscpobs ,r51.hcfechres as fecha_y_hora_aplicacion,case when h51.hcresult <> '' then h51.hcresult else des2.hcdscatr  end resultados,concat(maemed11.mmcedm ,maemed11.mmnomm ) as realizado_por, maemed1.mmnomm medico_interpreta, h51.hcfehint fecha_interpreta, h51.hcintres interpretacion " \
                  "from hosvital.hccom5 h5 inner join hosvital.hccom51 h51 on (h51.histipdoc=h5.histipdoc and h51.hisckey=h5.hisckey and h51.hiscsec= h5.hiscsec and h51.hcprccod = h5.hcprccod) " \
                  "inner join hosvital.hccom1 h1 on (h1.histipdoc=h5.histipdoc and h1.hisckey=h5.hisckey and h1.hiscsec= h5.hiscsec) left   join hosvital.hccom51R  r51 on (r51.histipdoc=h5.histipdoc and r51.hisckey=h1.hisckey and r51.hiscsec= h5.hiscsec and r51.hcprccns =  h51.hcprccns and r51.hcprccod = h5.hcprccod " \
                  "and r51.hcconres = (select max(h511r.hcconres) from hosvital.hccom51r  h511r where h511r.histipdoc=h5.histipdoc and h511r. hisckey=h5.hisckey and h511r.hiscsec = h5.hiscsec and h511r.hcprccod = r51.hcprccod)) " \
                  "left join hosvital.hccom2des des2 on (des2.histipdoc=h5.histipdoc and des2.hisckey=h1.hisckey and des2.hiscsec= h5.hiscsec and des2.hcprccod = h5.hcprccod and des2.hcprccns =  h51.hcprccns and des2.hcdesatr='HCResult' ) " \
                  "left join hosvital.maepro maepro on (maepro.prcodi= h5.hcprccod) left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h51.hcmedint) " \
                  "left join hosvital.maemed1 maemed11 on (maemed11.mmusuario= h51.rprusrrgs) wHere  h5.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(
            folio) + " and h5.hcprctip=1 and h51.hcprccns= (select max(h511.hcprccns) from hosvital.hccom51 h511 where h511.histipdoc=h51.histipdoc and h511.hisckey=h51.hisckey and  h511.hiscsec=h51.hiscsec and h511.hcprccod = h51.hcprccod) order by 2 "


        cursorI = con10.cursor()
        cursorI.execute(comando)
        rowsImagen = cursorI.fetchall()

        if rowsImagen == []:
            return localImagen
        else:
            localImagen = localImagen + 1


            texto1 = 'ORDENES DE IMAGENES DIAGNOSTICAS'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("descripcion", subtitle_atencion)
                         ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 12 * cm])

            localImagen = localImagen + 3
            Story.append(tbl1)
            rx = ''
            rx1 = ''
            resul = ''
            resul1 = ''
            for rowImagen in rowsImagen:
                rx1 = str(rowImagen.DESCRIPCION)
                resul1 = str(rowImagen.RESULTADOS)

                if rx == '' or rx1 != rx:
                    Story.append(Paragraph(str(rowImagen.HISCPOBS).replace("\n", "<br />"), subtitle_atencion))
                    tbl_data = [
                        [Paragraph(str(rowImagen.CANTIDAD), subtitle_atencion),
                         Paragraph(str(rowImagen.DESCRIPCION), subtitle_atencion),
                         Paragraph(str(rowImagen.ESTADO), subtitle_atencion),
                         # Paragraph("", headline_mayor33),
                         ]]
                    localImagen = localImagen + 1

                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)
                    Story.append(Paragraph('Fecha y hora de Aplicacion: ' + str(rowImagen.FECHA_Y_HORA_APLICACION),
                                           subtitle_atencion))
                    Story.append(Paragraph('Resultados: ', subtitle_atencion))

                    rx = rx1

                if resul == '' or resul1 != resul:

                    Story.append(Paragraph(str(rowImagen.RESULTADOS).replace("\n", "<br />"), subtitle_atencion))

                    #if rowImagen.REALIZADO_POR != '':
                    Story.append(Paragraph('Realizado Por: ' + str(rowImagen.REALIZADO_POR), subtitle_atencion))

                    if rowImagen.MEDICO_INTERPRETA != '':
                        Story.append(Paragraph('INTERPRETACION: ', subtitle_atencion))
                        Story.append(Spacer(1, 1))
                        Story.append(Paragraph(
                            'Interpretado por: ' + str(rowImagen.MEDICO_INTERPRETA) + str(rowImagen.FECHA_INTERPRETA),
                            subtitle_atencion))
                        Story.append(Paragraph(str(rowImagen.INTERPRETACION), subtitle_atencion))

                    resul = resul1
                else:
                    pass



        Story.append(Spacer(1, 1))
        localRegistro = self.registro(doc, localImagen, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                      headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        Story.append(Spacer(1, 1))

        localImagen = localImagen + 2
        con10.close()
        return localImagen


    def procNoQx(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Triage
        localprocNoQx = y
        print("Entre Procedimientos No Qx con localprocNoQx  folio y = ", localprocNoQx, folio, y)


        localprocNoQx = self.cabezote(doc, localprocNoQx, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 , headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento,0)

        con11 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio, h1.hisfhorat as fecha_folio,h5.hiscpcan cantidad,maepro.prnomb,case  when h5.hcprstgr='C' THEN 'Cancelado'  when h5.hcprstgr='N' THEN 'No se realizo'  when h5.hcprstgr='E' THEN 'En  proceso' " \
                  "when h5.hcprstgr='A' THEN 'Realizado'  when h5.hcprstgr='O' THEN 'Pendiente' when h5.hcprstgr='I' THEN 'Interpretado'  when h5.hcprstgr='E' THEN 'Pendiente' END estado , " \
                  "h5.hiscpobs descripcion, r51.hcfechres as fecha_y_hora_aplicacion, case when h51.hcresult <> '' then h51.hcresult else des2.hcdscatr  end resultados,  concat(maemed11.mmcedm ,maemed11.mmnomm ) as realizado_por, " \
                  "maemed1.mmnomm medico_interpreta, h51.hcfehint fecha_interpreta, h51.hcintres as interpretacion from hosvital.hccom5 h5 inner join hosvital.hccom51 h51 on (h51.histipdoc=h5.histipdoc and h51.hisckey=h5.hisckey 	" \
                  "and h51.hiscsec= h5.hiscsec and h51.hcprccod = h5.hcprccod) inner join hosvital.hccom1 h1 on (h1.histipdoc=h5.histipdoc and h1.hisckey=h5.hisckey and h1.hiscsec= h5.hiscsec) left join hosvital.hccom51R  r51 on " \
                  "(r51.histipdoc=h5.histipdoc and r51.hisckey=h1.hisckey and r51.hiscsec= h5.hiscsec and r51.hcprccns =  h51.hcprccns  and r51.hcprccod = h5.hcprccod) inner join hosvital.maepro maepro on (maepro.prcodi= h5.hcprccod) " \
                  "left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h51.hcmedint) left join hosvital.maemed1 maemed11 on (maemed11.mmusuario= h51.rprusrrgs ) left join hosvital.hccom2des des2 on " \
                  "(des2.histipdoc=h51.histipdoc and des2.hisckey=h51.hisckey and des2.hiscsec= h51.hiscsec and des2.hcprccod = h51.hcprccod and des2.hcprccns =  h51.hcprccns and des2.hcdesatr='HCResult' ) " \
                  "wHere  h5.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(folio) + " and  h5.hcprctip =  4 order by h5.hcprccod"

        cursorprocNoQx = con11.cursor()
        cursorprocNoQx.execute(comando)
        rowsNoQx = cursorprocNoQx.fetchall()


        if rowsNoQx == []:
            return localprocNoQx
        else:
            localprocNoQx = localprocNoQx + 1


            Story.append(Spacer(1, 2))
            texto1 = 'ORDENES DE PROCEDIMIWENTO NO QUIRURGICO'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("descripcion", subtitle_atencion)
                         ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 12 * cm])

            localprocNoQx = localprocNoQx + 3


            Story.append(tbl1)
            rx = ''
            rx1 = ''
            resul = ''
            resul1 = ''
            for rowNoQx in rowsNoQx:
                rx1 = str(rowNoQx.DESCRIPCION)
                resul1 = str(rowNoQx.RESULTADOS)

                if rx == '' or rx1 != rx:
                    #Story.append(Paragraph(str(rowNoQx.HISCPOBS), subtitle_atencion))
                    tbl_data = [
                        [Paragraph(str(rowNoQx.CANTIDAD), subtitle_atencion),
                         Paragraph(str(rowNoQx.PRNOMB), subtitle_atencion),
                         Paragraph(str(rowNoQx.ESTADO), subtitle_atencion),
                         # Paragraph("", headline_mayor33),
                         ]]
                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)
                    localprocNoQx = localprocNoQx + 1


                    Story.append(Paragraph('Fecha y hora de Aplicacion: ' + str(rowNoQx.FECHA_Y_HORA_APLICACION),
                                           subtitle_atencion))
                    Story.append(Paragraph('Resultados: ', subtitle_atencion))

                    rx = rx1

                if resul == '' or resul1 != resul:

                    Story.append(Paragraph(str(rowNoQx.RESULTADOS).replace("\n", "<br />"), subtitle_atencion))

                    #if rowImagen.REALIZADO_POR != '':
                    Story.append(Paragraph('Realizado Por: ' + str(rowNoQx.REALIZADO_POR), subtitle_atencion))

                    if rowNoQx.MEDICO_INTERPRETA != '':
                        Story.append(Paragraph('INTERPRETACION: ', subtitle_atencion))
                        Story.append(Spacer(1, 1))
                        Story.append(Paragraph(
                            'Interpretado por: ' + str(rowNoQx.MEDICO_INTERPRETA) + str(rowNoQx.FECHA_INTERPRETA),
                            subtitle_atencion))
                        Story.append(Paragraph(str(rowNoQx.INTERPRETACION), subtitle_atencion))

                    resul = resul1
                else:
                    pass


                localprocNoQx=localprocNoQx+7
        con11.close()
        localprocNoQx = self.registro(doc, localprocNoQx, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,    subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        return localprocNoQx


    def terapias(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Triage
        localTerapias = y
        print("Entre Terapias No Qx con localTerapias  folio y = ", localTerapias, folio, y)



        localTerapias = self.cabezote(doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 , headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento,0)

        con12 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio,  h5.hcprccod ,h1.hisfhorat as fecha_folio,h5.hiscpcan cantidad , maepro.prnomb,case when h5.hcprstgr='C' THEN 'Cancelado'  when h5.hcprstgr='N' THEN 'No se realizo'  when h5.hcprstgr='E' " \
                  "THEN 'En Proceso' when h5.hcprstgr='A' THEN 'Realizado' when h5.hcprstgr='O' THEN 'Pendiente' when h5.hcprstgr='I' THEN 'Interpretado' END estado,h5.hiscpobs descripcion,h51.hcfchrap  as fecha_y_hora_aplicacion, " \
                  "h51.hcresult resultados,concat(maemed11.mmcedm ,maemed11.mmnomm ) as realizado_por, maemed1.mmnomm medico_interpreta, h51.hcfehint fecha_interpreta,  h51.hcintres interpretacion from hosvital.hccom5 h5 " \
                  "inner  join hosvital.hccom51 h51 on (h51.histipdoc=h5.histipdoc and h51.hisckey=h5.hisckey and h51.hiscsec= h5.hiscsec and h51.hcprccod = h5.hcprccod and h5.hcprstgr<>'C' and ( (h51.hcresult<>'' and  h5.hcprstgr <> " \
                  "'N' ) or  (h51.hcresult = '' and  h5.hcprstgr not in ('N')))) inner join hosvital.hccom1 h1 on (h1.histipdoc=h5.histipdoc and h1.hisckey=h5.hisckey and h1.hiscsec= h5.hiscsec) inner join hosvital.hccom51R  r51 on  " \
                  "(r51.histipdoc=h5.histipdoc and r51.hisckey=h1.hisckey and r51.hiscsec= h5.hiscsec and r51.hcprccns =  h51.hcprccns  and r51.hcprccod = h5.hcprccod) inner join hosvital.maepro maepro on (maepro.prcodi= h5.hcprccod) " \
                  "left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h51.hcmedint) left join hosvital.maemed1 maemed11 on (maemed11.mmusuario= h51.rprusrrgs) " \
                 "wHere  h5.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(
                 folio) + " and  h5.hcprctip =  3 and h51.hcresult <> '' UNION select h1.hiscsec as folio,  h5.hcprccod, h1.hisfhorat as fecha_folio,h5.hiscpcan cantidad , " \
                  "maepro.prnomb,case when h5.hcprstgr='C' THEN 'Cancelado'  when h5.hcprstgr='N' THEN 'No se realizo' when h5.hcprstgr='E' THEN 'En Proceso' when h5.hcprstgr='A' THEN 'Realizado'  when h5.hcprstgr='O' THEN " \
                 "'Pendiente'   when h5.hcprstgr='I' THEN 'Interpretado'  END estado,  h5.hiscpobs descripcion,h51.hcfchrap  as fecha_y_hora_aplicacion ,des2.hcdscatr resultados,   " \
                "concat(maemed11.mmcedm ,maemed11.mmnomm ) as realizado_por, maemed1.mmnomm medico_interpreta, h51.hcfehint fecha_interpreta,  h51.hcintres interpretacion " \
                "from hosvital.hccom5 h5 inner join hosvital.hccom51 h51 on (h51.histipdoc=h5.histipdoc and h51.hisckey=h5.hisckey and h51.hiscsec= h5.hiscsec and h51.hcprccod = h5.hcprccod and h5.hcprstgr<>'C' ) " \
                "inner join hosvital.hccom1 h1 on (h1.histipdoc=h5.histipdoc and h1.hisckey=h5.hisckey and h1.hiscsec= h5.hiscsec) inner join hosvital.maepro maepro on (maepro.prcodi= h5.hcprccod) " \
                "left join hosvital.hccom2des des2 on (des2.histipdoc=h5.histipdoc and des2.hisckey=h1.hisckey and des2.hiscsec= h5.hiscsec and des2.hcprccod = h5.hcprccod and des2.hcprccns =  h51.hcprccns ) " \
                "left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h51.hcmedint) left join hosvital.maemed1 maemed11 on (maemed11.mmusuario= h51.rprusrrgs) " \
                "wHere  h5.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(
               folio) + " and  h5.hcprctip =  3   and des2.hcdesatr='HCResult'  order by 2"

        cursorT = con12.cursor()
        cursorT.execute(comando)
        rowsTerapias = cursorT.fetchall()

        if rowsTerapias == []:
            return localTerapias
        else:
            localTerapias = localTerapias + 1
            Story.append(Spacer(1, 2))

            texto1 = 'TERAPIAS'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("Descripcion", subtitle_atencion),Paragraph("Estado", subtitle_atencion),   ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 10 * cm, 5 * cm])

            localTerapias = localTerapias + 3

            Story.append(tbl1)
            rx = ''
            rx1 = ''
            resul = ''
            resul1 = ''
            for rowTerapias in rowsTerapias:
                rx1 = str(rowTerapias.DESCRIPCION)
                resul1 = str(rowTerapias.RESULTADOS)

                if rx == '' or rx1 != rx:
                    #Story.append(Paragraph(str(rowTerapias.HISCPOBS), subtitle_atencion))
                    tbl_data = [
                        [Paragraph(str(rowTerapias.CANTIDAD), subtitle_atencion),
                         Paragraph(str(rowTerapias.PRNOMB), subtitle_atencion),
                         Paragraph(str(rowTerapias.ESTADO), subtitle_atencion),
                         # Paragraph("", headline_mayor33),
                         ]]
                    localTerapias = localTerapias + 1

                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)
                    Story.append(Paragraph(str(rowTerapias.DESCRIPCION),   subtitle_atencion))
                    Story.append(Paragraph('Fecha y hora de Aplicacion: ' + str(rowTerapias.FECHA_Y_HORA_APLICACION),
                                           subtitle_atencion))
                    Story.append(Paragraph('Resultados: ', subtitle_atencion))

                    rx = rx1

                if resul == '' or resul1 != resul:

                    Story.append(Paragraph(str(rowTerapias.RESULTADOS).replace("\n", "<br />"), subtitle_atencion))

                    #if rowImagen.REALIZADO_POR != '':
                    Story.append(Paragraph('Realizado Por: ' + str(rowTerapias.REALIZADO_POR), subtitle_atencion))

                    if rowTerapias.MEDICO_INTERPRETA != '':
                        Story.append(Paragraph('INTERPRETACION: ', subtitle_atencion))
                        Story.append(Spacer(1, 1))
                        Story.append(Paragraph(
                            'Interpretado por: ' + str(rowTerapias.MEDICO_INTERPRETA) + str(rowTerapias.FECHA_INTERPRETA),
                            subtitle_atencion))
                        Story.append(Paragraph(str(rowTerapias.INTERPRETACION), subtitle_atencion))

                    resul = resul1
                else:
                    pass

        Story.append(Spacer(1, 1))
        localRegistro = self.registro(doc, localTerapias, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                      headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        Story.append(Spacer(1, 1))

        localTerapias = localTerapias + 2
        con12.close()
        return localTerapias


    def terapiasGases(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Triage

        localTerapiasGases = y

        print("Entre Terapias Gases No Qx con localTerapiasGases  folio y = ", localTerapiasGases, folio, y)


        print (localTerapiasGases)
        localTerapiasGases = self.cabezote(doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 , headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento,0)

        con13 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio,  h5.hcprccod ,h1.hisfhorat as fecha_folio,h5.hiscpcan cantidad , maepro.prnomb,case when h5.hcprstgr='C' THEN 'Cancelado'  when h5.hcprstgr='N' THEN 'No se realizo' " \
                  "when h5.hcprstgr='E' THEN 'En Proceso'  when h5.hcprstgr='A' THEN 'Realizado'  when h5.hcprstgr='O' THEN 'Pendiente' when h5.hcprstgr='I' THEN 'Interpretado'  END estado,h5.hiscpobs descripcion, " \
                  "h51.hcfchrap  as  fecha_y_hora_aplicacion,  " \
                  "prc.prbdsc  as analisis,rs.rprtext    resultados,prc.rngnml as valores_referencia,concat(maemed11.mmcedm ,maemed11.mmnomm ) as realizado_por, maemed1.mmnomm medico_interpreta, h51.hcfehint fecha_interpreta, " \
                  "h51.hcintres interpretacion from hosvital.hccom5 h5 inner join hosvital.hccom51 h51 on (h51.histipdoc=h5.histipdoc and h51.hisckey=h5.hisckey and h51.hiscsec= h5.hiscsec and h51.hcprccod = h5.hcprccod and  " \
                  "h5.hcprstgr<>'C' and ( (h51.hcresult<>'' and  h5.hcprstgr <>  'N' ) or  (h51.hcresult = '' and  h5.hcprstgr not in ('N')))) inner join hosvital.hccom1 h1 on (h1.histipdoc=h5.histipdoc and h1.hisckey=h5.hisckey and h1.hiscsec=  " \
                  "h5.hiscsec) inner join hosvital.hccom51R r51 on(r51.histipdoc = h5.histipdoc and r51.hisckey = h1.hisckey and r51.hiscsec = h5.hiscsec and r51.hcprccns = h51.hcprccns and r51.hcprccod = h5.hcprccod) " \
                  "inner join hosvital.maepro  maepro on (maepro.prcodi = h5.hcprccod) inner join  hosvital.rslprc1 rs  on (rs.histipdoc = h5.histipdoc and rs.hisckey = h5.hisckey and rs.hiscsec = h5.hiscsec and rs.hcprccod = h5.hcprccod) " \
                 "left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h51.hcmedint)  left join hosvital.maemed1 maemed11 on (maemed11.mmusuario = h51.rprusrrgs) " \
                "inner join hosvital.prbxprc prc on  (prc.prcodi = maepro.prcodi and prc.prbcod = rs.prbcod) wHere         h5.histipdoc = '" + tipodoc + "' and h1.hisckey = '" + documento + "' and h1.hiscsec = " + str(folio) + " and h5.hcprctip = 3"

        cursorTT = con13.cursor()
        cursorTT.execute(comando)
        rowsTerapiasGases = cursorTT.fetchall()

        if rowsTerapiasGases == []:
            return localTerapiasGases
        else:
            localTerapiasGases = localTerapiasGases + 1

            Story.append(Spacer(1, 2))

            #texto1 = 'TERAPIAS'
            #Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            #tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("Descripcion", subtitle_atencion),Paragraph("Estado", subtitle_atencion),   ]]

            #tbl1 = Table(tbl_data, colWidths=[4 * cm, 10 * cm, 5 * cm])

            localTerapiasGases = localTerapiasGases + 3

            #Story.append(tbl1)
            rx = ''
            rx1 = ''
            resul = ''
            resul1 = ''
            tbl_data = [
                [Paragraph("ANALISIS", headline_mayor4),
                 Paragraph("RESULTADO", headline_mayor4),
                 Paragraph("UNIDAD", headline_mayor4),
                 Paragraph("VALORES RF", headline_mayor4),
                 ]]
            tbl1 = Table(tbl_data, colWidths=[7 * cm, 5 * cm, 2 * cm, 3 * cm])
            Story.append(tbl1)
            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))

            for rowTerapiasGases in rowsTerapiasGases:
                rx1 = str(rowTerapiasGases.PRNOMB)
                resul1 = str(rowTerapiasGases.RESULTADOS)

                if rx == '' or rx1 != rx:

                    tbl_data = [
                        [Paragraph(str(rowTerapiasGases.CANTIDAD), subtitle_atencion),
                         Paragraph(str(rowTerapiasGases.PRNOMB), subtitle_atencion),
                         Paragraph(str(rowTerapiasGases.ESTADO), subtitle_atencion),
                         # Paragraph("", headline_mayor33),
                         ]]
                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)
                    localTerapiasGases = localTerapiasGases + 1

                    Story.append(Paragraph('RESULTADOS: ', headline_mayor))
                    Story.append(Spacer(1, 1))
                    rx = rx1

                if resul == '' or resul1 != resul:
                    tbl_data = [
                        [Paragraph(str(rowTerapiasGases.ANALISIS), subtitle_atencion),
                         Paragraph(str(rowTerapiasGases.RESULTADOS).replace("\n", "<br />"), subtitle_atencion),
                         Paragraph("", headline_mayor33),
                         Paragraph(str(rowTerapiasGases.VALORES_REFERENCIA).replace("\n", "<br />"),
                                   subtitle_atencion)]]

                    tbl1 = Table(tbl_data, colWidths=[7 * cm, 5 * cm, 2 * cm, 3 * cm])
                    Story.append(tbl1)

                    resul = resul1





        Story.append(Spacer(1, 1))
        localRegistro = self.registro(doc, localTerapiasGases, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                      headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        Story.append(Spacer(1, 1))

        localTerapiasGases = localTerapiasGases + 2
        con13.close()
        return localTerapiasGases

    def interconsultas(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,subtitle_cabezote, subtitle_nacimiento):

        # Trae Interconsulta
        localInterconsulta = y
        print("Entre Intgerconsultas Gases No Qx con localInterconsulta  folio y = ", localInterconsulta, folio, y)
        con14 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  h1.hiscsec as folio,  concat('INTERCONSULTA POR ',esp.menome ) Descripcion,  date(h1.hisfhorat) as fecha_orden,   case when i.intest='A' then 'Atendido'  when i.intest='O' then 'Ordenada' when i.intest='P' then " \
                  "'Pendiente' end estado, i.intobsord OBSERVACIONES,   i.intdscrsl as Resultados, i.intfchrsl, concat('RELIZADO POR ',maemed1.mmnomm) ,    concat('Reg: ', maemed1.mmregm ),esp.menome as especialidad, " \
                  " maemed1.mmfirma as ruta_firma from hosvital.intercn i inner join hosvital.hccom1 h1 on (h1.histipdoc= i.histipdoc and h1.hisckey=i.hisckey and h1.hiscsec=i.hiscsec) inner join hosvital.maeesp esp on (esp.mecode= " \
                  "i.mecode) LEFT join hosvital.maemed1 maemed1 on (maemed1.mmusuario=i.intusrrsp) where  i.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(folio)


        cursorTTT = con14.cursor()
        cursorTTT.execute(comando)
        rowsInterconsulta = cursorTTT.fetchall()

        if rowsInterconsulta == []:
            return localInterconsulta
        else:
            texto1 = 'INTERCONSULTAS'
            Story.append(Paragraph(texto1, headline_mayor))

            for rowInterconsulta in rowsInterconsulta:
                localInterconsulta = localInterconsulta + 1
                Story.append(Spacer(1, 5))

                localInterconsulta = localInterconsulta + 4
                Story.append(Spacer(1, 4))
                tbl_data = [
                    [Paragraph(str(rowInterconsulta.DESCRIPCION).replace("\n", "<br />"), subtitle_cabezote),
                     Paragraph(str(rowInterconsulta.FECHA_ORDEN), subtitle_cabezote),
                     Paragraph("Fecha De Orden", subtitle_cabezote),
                     Paragraph(str(rowInterconsulta.ESTADO), headline_mayor4),
                     Paragraph("", headline_mayor4),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[8 * cm, 3 * cm, 3 * cm, 3 * cm, 1 * cm])
                Story.append(tbl1)


                texto1 = 'OBSERVACIONES'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 2))
                Story.append(Paragraph(str(rowInterconsulta.OBSERVACIONES).replace("\n", "<br />"), subtitle_atencion))
                Story.append(Spacer(1, 4))

                texto1 = 'RESULTADOS'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 2))
                Story.append(Paragraph(str(rowInterconsulta.RESULTADOS).replace("\n", "<br />"), subtitle_atencion))
                Story.append(Spacer(1, 4))

                # Story.append(Spacer(1, 2))
                localInterconsulta = localInterconsulta + 7

        con14.close()
        localRegistro = self.registro(doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1,
                                      headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        return localInterconsulta

    def cirugias(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2,
                 headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,
                 subtitle_cabezote, subtitle_nacimiento):

        # Trae Interconsulta
        localcirugias = y
        print("Entre Cirugias Gases No Qx con localcirugias  folio y = ", localcirugias, folio, y)

        con14 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select p.procircod,h1.histipdoc,h1.hisckey,h1.hiscsec folio,h1.hisfhorat as fecha,case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end tipo_atencion,p1.crgcnt as cantidad,p1.crgcod codigo,m.prnomb descripcion, " \
                  "(select m2.mpngrp from hosvital.maeate m inner join hosvital.maeate2 m2 on (m2.mpnfac=m.mpnfac) where m.mptdoc=h1.histipdoc  and m.mpcedu= h1.hisckey and m.mactving= h1.hctvin1 and m2.prcodi=p1.crgcod AND m2.MAHONCOD='01' " \
                  "group by m2.mpngrp)  as Grupo_Quirurgico_facturado,(select t1.tfngrp from hosvital.tmpfac t inner join hosvital.tmpfac1 t1 on (t1.tftdoc = t.tftdoc and t1.tfcedu=t.tfcedu and t1.tmctving= t.tmctving  and  t1.tfptpotrn = 'F' AND t1.tfhnrcod='01' ) " \
                  "where  t.tftdoc =h1.histipdoc  and t.tfcedu= h1.hisckey and t.tmctving= h1.hctvin1   and t1.tfprc1=p1.crgcod group by t1.tfngrp) as Grupo_Quirurgico_acostado, concat(concat (m1.mmcodm,' ') , m1.mmnomm) as medico, esp.menome as especialidad,m11.mmcodm ,m11.mmnomm medico_cirugia, esp11.menome as especialida, " \
                  "edia.dmcodi diag1,edia.dmnomb as diag_preoperatorio,edia11.dmcodi diag2,edia11.dmnomb as diag_postoperatorio,case when d.tipher=1 then 'LIMPIA' when d.tipher=2 then 'LIMPIA CONTAMINADA' else 'Otra' end  as tipo_herida,case   when d.tipane='S' then 'SEDACION'  when d.tipane='G' then 'GENERAL'  when d.tipane='R' then 'REGIONAL' when d.tipane='L' then 'LOCAL' else 'Otro tipo' end  as tipo_anestesia, " \
                  "'' TIPO_CIRUGIA, d.cansan as cantidad_sangrado,'ml' MEDIDA,case when d.viaing='D' then 'Diferente Via'  when d.viaing='U' then 'Unica Via'  end  as Via1,v.viadsc as via, d.fecinicir as Realizacion_acto_Quirurgico, d.horinicir as hora_inicio, d.horfincir as  hora_final, tieper as tiempo_perfusion,d.tieclamp as tiempo_clamp, 'Minuto', " \
                  "d.descir as descripcion_quirurgica,case  when d.DesIndCom ='N' then 'No' when d.DesIndCom ='S' then 'Si'  end as Complicaciones, d.deshalenc as hallazgos, case when tej.coddestej  <> '' then 'Si' else 'No' end as enviado_a_patologia, tej.coddestej " \
                  "from hosvital.hccom1 h1 inner  join hosvital.procir p on (p.mptdoc = h1.histipdoc and p.mpcedu=h1.hisckey and p.proctvin = h1.hctvin1 and p.proflicx = h1.hiscsec ) " \
                  "inner join hosvital.procir1 p1 on (p1.procircod=p.procircod) inner join hosvital.maepro m on (m.prcodi=p1.crgcod) left join hosvital.procir2 p2 on (p2.procircod=p1.procircod and p2.perstip='01') left join hosvital.maemed1 m1 on (m1.mmcodm = p2.perscod ) " \
                  "left join hosvital.maeesp esp on (esp.mecode=p2.persesp) inner join hosvital.vias v on (v.viacod  = p1.viacod) inner join hosvital.descirmed d on (d.codcir = p.procircod) " \
                  "inner join hosvital.maemed1 m11 on (m11.mmcodm = d.codmed) inner join hosvital.maeesp esp11 on (esp11.mecode=d.codesp) inner join hosvital.maedia edia on (edia.dmcodi=d.diaent)  inner join hosvital.maedia edia11 on (edia11.dmcodi=d.diasal) " \
                  "left join hosvital.DesCirTej  tej on (tej.codcir=d.codcir) where h1.histipdoc='" + tipodoc + "' and h1.hisckey = '" + documento + "' and h1.hiscsec = " + str(folio) + " order by h1.hiscsec"

        cursorCir = con14.cursor()
        cursorCir.execute(comando)
        rowsCirugia = cursorCir.fetchall()

        if rowsCirugia == []:
            return localcirugias
        else:
            Story.append(Spacer(1, 4))
            texto1 = 'CIRUGIAS'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [
                [Paragraph("CANT", headline_mayor4),
                 Paragraph("CODIGO", headline_mayor4),
                 Paragraph("DESCRIPCION", headline_mayor4),
                 Paragraph("Grupo Quirrugico", headline_mayor4),
                 Paragraph("", headline_mayor4),
                 ]]
            tbl1 = Table(tbl_data, colWidths=[3 * cm, 3 * cm, 8 * cm, 4 * cm, 1 * cm])
            Story.append(tbl1)

            for rowCirugia in rowsCirugia:
                localcirugias = localcirugias + 1
                Story.append(Spacer(1, 5))

                tbl_data = [
                    [Paragraph(str(rowCirugia.CANTIDAD), subtitle_atencion),
                     Paragraph(str(rowCirugia.CODIGO), subtitle_atencion),
                     Paragraph(str(rowCirugia.DESCRIPCION), subtitle_atencion),
                     Paragraph(str(rowCirugia.GRUPO_QUIRURGICO_ACOSTADO), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[3 * cm, 3 * cm, 8 * cm, 4 * cm, 1 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Medico:", subtitle_cabezote),
                     Paragraph(str(rowCirugia.MEDICO), subtitle_atencion),
                     Paragraph("Especialidad:", subtitle_cabezote),
                     Paragraph(str(rowCirugia.ESPECIALIDAD), subtitle_atencion),
                     Paragraph("Via:", subtitle_cabezote),
                     Paragraph(str(rowCirugia.VIA), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[2 * cm, 5 * cm, 2 * cm, 5 * cm, 2 * cm,2 * cm, 1 * cm])
                Story.append(tbl1)

                texto1 = '_______________________________________________________________________________________________'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 1))

            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 3))
            texto1 = 'DESCRIPCION CIRUGIA'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [
                    [Paragraph("Medico:", headline_mayor),
                     Paragraph(str(rowCirugia.MEDICO), subtitle_atencion),
                     Paragraph("Especialidad:", headline_mayor),
                     Paragraph(str(rowCirugia.ESPECIALIDA), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
            tbl1 = Table(tbl_data, colWidths=[2 * cm, 6 * cm, 3 * cm, 5 * cm, 3 * cm])
            Story.append(tbl1)

            tbl_data = [
                    [Paragraph("Diagnostico Preoperatorio:", headline_mayor),
                     Paragraph(str(rowCirugia.DIAG1), subtitle_atencion),
                     Paragraph(str(rowCirugia.DIAG_PREOPERATORIO), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
            tbl1 = Table(tbl_data, colWidths=[8 * cm, 3 * cm, 7 * cm, 1 * cm])
            Story.append(tbl1)

            tbl_data = [
                    [Paragraph("Diagnostico Postoperatorio:", headline_mayor),
                     Paragraph(str(rowCirugia.DIAG2), subtitle_atencion),
                     Paragraph(str(rowCirugia.DIAG_POSTOPERATORIO), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
            tbl1 = Table(tbl_data, colWidths=[8 * cm, 3 * cm, 7 * cm, 1 * cm])
            Story.append(tbl1)

            tbl_data = [
                    [Paragraph("Tipo de Herida:", headline_mayor),
                     Paragraph(str(rowCirugia.TIPO_HERIDA), subtitle_atencion),
                     Paragraph("Tipo de Anestesia:", headline_mayor),
                     Paragraph(str(rowCirugia.TIPO_ANESTESIA), subtitle_atencion),
                     Paragraph("Tipo de Cirugia:", headline_mayor),
                     Paragraph(str(rowCirugia.TIPO_CIRUGIA), subtitle_atencion),
                     Paragraph("", headline_mayor),
                    ]]
            tbl1 = Table(tbl_data, colWidths=[3 * cm, 2 * cm, 4 * cm, 3 * cm, 4 * cm,2 * cm,1 * cm])
            Story.append(tbl1)

            tbl_data = [
                    [Paragraph("Cantidad de Sangrado:", headline_mayor),
                     Paragraph(str(rowCirugia.CANTIDAD_SANGRADO), subtitle_atencion),
                     Paragraph(str(rowCirugia.MEDIDA), subtitle_atencion),
                     Paragraph("Via:", headline_mayor),
                     Paragraph(str(rowCirugia.VIA1), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
            tbl1 = Table(tbl_data, colWidths=[6 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 1 * cm])
            Story.append(tbl1)

            tbl_data = [
                    [Paragraph("Realizacion Acto Quirurgico:", headline_mayor),
                     Paragraph(str(rowCirugia.REALIZACION_ACTO_QUIRURGICO), subtitle_atencion),
                     Paragraph("Hora Inicio:", headline_mayor),
                     Paragraph(str(rowCirugia.HORA_INICIO), subtitle_atencion),
                     Paragraph("Hora Final:", headline_mayor),
                     Paragraph(str(rowCirugia.HORA_FINAL), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
            tbl1 = Table(tbl_data, colWidths=[5.5 * cm, 2 * cm, 2.5 * cm, 3 * cm,2.5 * cm, 3 * cm, 0.5 * cm])
            Story.append(tbl1)

            tbl_data = [
                    [Paragraph("Tiempo de Perfusion:", headline_mayor),
                     Paragraph(str(rowCirugia.TIEMPO_PERFUSION), subtitle_atencion),
                     Paragraph("Tiempo de Clamp:", headline_mayor),
                     Paragraph(str(rowCirugia.TIEMPO_CLAMP), subtitle_atencion),
                     Paragraph("Minuto", headline_mayor),
                     ]]
            tbl1 = Table(tbl_data, colWidths=[6 * cm, 3 * cm, 5 * cm, 3 * cm, 2 * cm])
            Story.append(tbl1)

            Story.append(Spacer(1, 1))

            texto1 = 'Descripcion Quirurgica'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 4))
            Story.append(Paragraph(str(rowCirugia.DESCRIPCION_QUIRURGICA).replace("\n", "<br />"), subtitle_atencion))
            Story.append(Spacer(1, 3))

            if rowCirugia.COMPLICACIONES == 'Si':
                 tbl_data = [
                    [Paragraph("Complicaciones:", headline_mayor),
                     Paragraph("SI", headline_mayor),
                     Paragraph(str(rowCirugia.COMPLICACIONES), subtitle_atencion),
                     Paragraph("NO", headline_mayor),
                     Paragraph("", headline_mayor),
                     Paragraph("", headline_mayor),
                    ]]
                 tbl1 = Table(tbl_data, colWidths=[6.5 * cm, 2 * cm, 3 * cm, 2 * cm, 3 * cm, 2.5 * cm])
                 Story.append(tbl1)

            if rowCirugia.COMPLICACIONES == 'No':
                 tbl_data = [
                    [Paragraph("Complicaciones:", headline_mayor),
                     Paragraph("SI", headline_mayor),
                     Paragraph("", headline_mayor),
                     Paragraph("NO", headline_mayor),
                     Paragraph(str(rowCirugia.COMPLICACIONES), subtitle_atencion),
                     Paragraph("", headline_mayor),
                    ]]
                 tbl1 = Table(tbl_data, colWidths=[6.5 * cm, 2 * cm, 3 * cm, 2 * cm, 3 * cm, 2.5 * cm])
                 Story.append(tbl1)


            Story.append(Spacer(1, 1))
            texto1 = 'Hallazgos:'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 3))
            Story.append(Paragraph(str(rowCirugia.HALLAZGOS), subtitle_atencion))
            Story.append(Spacer(1, 2))

            if rowCirugia.ENVIADO_A_PATOLOGIA == 'Si':
                tbl_data = [
                    [Paragraph("Tejidos enviados a patotogia : SI:", headline_mayor),
                     Paragraph(str(rowCirugia.ENVIADO_A_PATOLOGIA), subtitle_atencion),
                     Paragraph("NO", headline_mayor),
                     Paragraph("", subtitle_atencion),
                     Paragraph("", headline_mayor4),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[7.5 * cm, 2.5 * cm, 3 * cm, 2.5 * cm, 3 * cm, 0.5 * cm])
                Story.append(tbl1)

            if rowCirugia.ENVIADO_A_PATOLOGIA == 'No':
                tbl_data = [
                    [Paragraph("Tejidos enviados a patotogia : SI:", headline_mayor),
                     Paragraph("", subtitle_atencion),
                     Paragraph("NO", headline_mayor),
                     Paragraph(str(rowCirugia.ENVIADO_A_PATOLOGIA), subtitle_atencion),
                     Paragraph("", subtitle_atencion),
                     Paragraph("", headline_mayor4),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[7.5 * cm, 2.5 * cm, 3 * cm, 2.5 * cm, 3 * cm, 0.5 * cm])
                Story.append(tbl1)


            Story.append(Paragraph(str(rowCirugia.CODDESTEJ), subtitle_atencion))
            Story.append(Spacer(1, 1))

            texto1 = '_______________________________________________________________________________________________'
            Story.append(Paragraph(texto1, headline_mayor))

            localcirugias = localcirugias + 7

            localRegistro = self.registro(doc, localcirugias, Story, tipodoc, documento, folio, headline_mayor,
                                          headline_mayor1,
                                          headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                          subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)

        con14.close()

        con15 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando1 = "select h1.histipdoc,h1.hisckey,h1.hiscsec,p2.perscod,maemed1.mmnomm, case when p2.perstip='01' then 'Especialista Qx' when p2.perstip='05' then 'Ayudante' when p2.perstip='07' then 'Instrumentador' when p2.perstip='04' then 'Anestesiologo' end tipo, case when p2.persest='S' then 'Si' when p2.persest='N' then 'No'  else '' end participo " \
                  "from hosvital.hccom1 h1 inner join hosvital.procir p on (p.mptdoc = h1.histipdoc and p.mpcedu=h1.hisckey and p.proctvin = h1.hctvin1 and p.proflicx = h1.hiscsec ) " \
                  "inner join hosvital.procir2 p2 on (p2.procircod=p.procircod) inner join hosvital.maemed1 maemed1 on (maemed1.mmcodm = p2.perscod) where  h1.histipdoc='" + tipodoc + "' and h1.hisckey = '" + documento + "' and h1.hiscsec = " + str(folio) + " order by p2.perscod"

        cursor2Cir = con15.cursor()
        cursor2Cir.execute(comando1)
        rowsCirugia2 = cursor2Cir.fetchall()

        if rowsCirugia2 == []:
            return localcirugias
        else:
            Story.append(Spacer(1, 3))
            texto1 = 'OTROS PARTICIPANTES'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 3))

            tbl_data = [
                [Paragraph("CODIGO", headline_mayor4),
                 Paragraph("NOMBRE", headline_mayor4),
                 Paragraph("TIPO", headline_mayor4),
                 Paragraph("PARTICIPO?", headline_mayor4),
                 Paragraph("", headline_mayor4),
                 ]]
            tbl1 = Table(tbl_data, colWidths=[3 * cm, 7 * cm, 4 * cm, 4 * cm, 1 * cm])
            Story.append(tbl1)

            for rowCirugia2 in rowsCirugia2:
                localcirugias = localcirugias + 1
                Story.append(Spacer(1, 2))

                tbl_data = [
                    [Paragraph(str(rowCirugia2.PERSCOD), subtitle_atencion),
                     Paragraph(str(rowCirugia2.MMNOMM), subtitle_atencion),
                     Paragraph(str(rowCirugia2.TIPO), subtitle_atencion),
                     Paragraph(str(rowCirugia2.PARTICIPO), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[2 * cm, 8 * cm, 5 * cm, 2 * cm, 2 * cm])
                Story.append(tbl1)


        con15.close()

        return localcirugias



    def procQx(self, doc, y, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 ,headline_mayor3, headline_mayor33, headline_mayor4,subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento):

        # Trae Triage
        localprocQx = y
        print("Entre Proced Qx Gases No Qx con localprocQx  folio y = ", localprocQx, folio, y)
        localprocQx = self.cabezote(doc, localprocQx, Story, tipodoc, documento, folio,   headline_mayor, headline_mayor1, headline_mayor2 , headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,subtitle_atencion,subtitle_cabezote,subtitle_nacimiento,0)

        con16 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select h1.hiscsec as folio, h1.hisfhorat as fecha_folio,h5.hiscpcan cantidad,maepro.prnomb,case  when h5.hcprstgr='C' THEN 'Cancelado'  when h5.hcprstgr='N' THEN 'No se realizo'  when h5.hcprstgr='E' THEN 'En  proceso' " \
                  "when h5.hcprstgr='A' THEN 'Realizado'  when h5.hcprstgr='O' THEN 'Pendiente' when h5.hcprstgr='I' THEN 'Interpretado'  when h5.hcprstgr='E' THEN 'Pendiente' END estado , " \
                  "h5.hiscpobs descripcion, r51.hcfechres as fecha_y_hora_aplicacion, case when h51.hcresult <> '' then h51.hcresult else des2.hcdscatr  end resultados,  concat(maemed11.mmcedm ,maemed11.mmnomm ) as realizado_por, " \
                  "maemed1.mmnomm medico_interpreta, h51.hcfehint fecha_interpreta, h51.hcintres as interpretacion from hosvital.hccom5 h5 inner join hosvital.hccom51 h51 on (h51.histipdoc=h5.histipdoc and h51.hisckey=h5.hisckey 	" \
                  "and h51.hiscsec= h5.hiscsec and h51.hcprccod = h5.hcprccod) inner join hosvital.hccom1 h1 on (h1.histipdoc=h5.histipdoc and h1.hisckey=h5.hisckey and h1.hiscsec= h5.hiscsec) left join hosvital.hccom51R  r51 on " \
                  "(r51.histipdoc=h5.histipdoc and r51.hisckey=h1.hisckey and r51.hiscsec= h5.hiscsec and r51.hcprccns =  h51.hcprccns  and r51.hcprccod = h5.hcprccod) inner join hosvital.maepro maepro on (maepro.prcodi= h5.hcprccod) " \
                  "left join hosvital.maemed1 maemed1 on (maemed1.mmcodm = h51.hcmedint) left join hosvital.maemed1 maemed11 on (maemed11.mmusuario= h51.rprusrrgs ) left join hosvital.hccom2des des2 on " \
                  "(des2.histipdoc=h51.histipdoc and des2.hisckey=h51.hisckey and des2.hiscsec= h51.hiscsec and des2.hcprccod = h51.hcprccod and des2.hcprccns =  h51.hcprccns and des2.hcdesatr='HCResult' ) " \
                  "wHere  h5.histipdoc='" + tipodoc + "' and h1.hisckey='" + documento + "' and h1.hiscsec= " + str(folio) + " and  h5.hcprctip =  5 order by h5.hcprccod"

        cursorprocQx = con16.cursor()
        cursorprocQx.execute(comando)
        rowsQx = cursorprocQx.fetchall()


        if rowsQx == []:
            return localprocQx
        else:
            localprocQx = localprocQx + 1
            Story.append(Spacer(1, 2))
            texto1 = 'ORDENES DE PROCEDIMIENTOS QUIRURGICOS'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("descripcion", subtitle_atencion)
                         ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 12 * cm])

            localprocQx = localprocQx + 3

            Story.append(tbl1)
            rx = ''
            rx1 = ''
            resul = ''
            resul1 = ''

            for rowQx in rowsQx:
                rx1 = str(rowQx.DESCRIPCION)
                resul1 = str(rowQx.RESULTADOS)


                if rx == '' or rx1 != rx:

                    tbl_data = [
                        [Paragraph(str(rowQx.CANTIDAD), subtitle_atencion),
                         Paragraph(str(rowQx.PRNOMB), subtitle_atencion),
                         Paragraph(str(rowQx.ESTADO), subtitle_atencion),
                         # Paragraph("", headline_mayor33),
                         ]]
                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)
                    Story.append(Paragraph(str(rowQx.DESCRIPCION), subtitle_atencion))
                    localprocQx = localprocQx + 1


                    Story.append(Paragraph('Fecha y hora de Aplicacion: ' + str(rowQx.FECHA_Y_HORA_APLICACION),
                                           subtitle_atencion))
                    Story.append(Paragraph('Resultados: ', subtitle_atencion))
                    Story.append(Paragraph(str(rowQx.RESULTADOS).replace("\n", "<br />"), subtitle_atencion))
                    rx = rx1

                if resul == '' or resul1 != resul:
                    #if rowImagen.REALIZADO_POR != '':
                    Story.append(Paragraph('Realizado Por: ' + str(rowQx.REALIZADO_POR), subtitle_atencion))

                    if rowQx.MEDICO_INTERPRETA != '':
                        Story.append(Paragraph('INTERPRETACION: ', subtitle_atencion))
                        Story.append(Spacer(1, 1))
                        Story.append(Paragraph(
                            'Interpretado por: ' + str(rowQx.MEDICO_INTERPRETA) + str(rowQx.FECHA_INTERPRETA),
                            subtitle_atencion))
                        Story.append(Paragraph(str(rowQx.INTERPRETACION), subtitle_atencion))

                    resul = resul1
                else:
                    pass


                localprocQx=localprocQx+7
        con16.close()
        localprocQx = self.registro(doc, localprocQx, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol,    subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        return localprocQx

    def incapacidades(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2,
                      headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,
                      subtitle_cabezote, subtitle_nacimiento):

        # Trae Interconsulta
        localincapacidad = y
        print("Entre Incapacidades Qx Gases No Qx con localincapacidad  folio y = ", localincapacidad, folio, y)

        con17 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "SELECT'CERTIFICADO DE INCAPCIDAD', inc.incconpac incconpac, cap.mpnomc as nombre, cap.mptdoc, cap.mpcedu, hc.hcdxcod, day(inc.incfecreg) as dia,month(inc.incfecreg) as mes,year(inc.incfecreg) as ano,'Ocupacion' OCUPA, " \
                  "maeemp.menomb as empresa, caue.cedetall as tipo_incapacidad,cap.mpcedu as historia_clinica,inc.incfecini as fecha_inicia, inc.incfecfin as fecha_fin, IncDiaInc as dias_incapacidad ,    caue.cedetall  as causa_externa, case when inc.inctipate='01' then 'AMBULATORIA'    when inc.inctipate='02' then 'HOSPITALARIA'   when inc.inctipate='03' then 'URGENCIAS'  end as  tipo_atencion, 'procedimiento', 'Diagnostico a relacionar','fecha accidente de trabajo', " \
                  "case when IncProAfi='N' then 'No'  when IncProAfi='S' then 'Si' end AS prorroga, 'FUNDACION SAN CARLOS' AS EXPEDIDA_EN , ' ' AS EMPRESA_DONDE_TRABAJA, inc.IncObsMed AS OBSERVACION_PROFESIONAL, maemed1.mmnomm, maemed1.mmregm as Registro  , esp.menome as especialidad " \
                  "FROM hosvital.hccom1 h1 inner join hosvital.incpac inc on (inc.inctipdoc= h1.histipdoc and inc.INCDOCAFI= h1.hisckey and inc.INCCODFOL= h1.hiscsec) inner join hosvital.capbas cap on (cap.mptdoc = h1.histipdoc and cap.mpcedu=h1.hisckey) " \
                  "inner join hosvital.hcdiagn  hc on (hc.histipdoc=h1.histipdoc and hc.hisckey=h1.hisckey and hc.hiscsec=h1.hiscsec) inner join hosvital.ingresos i on (i.mptdoc = h1.histipdoc and i.mpcedu=h1.hisckey and i.ingcsc = h1.hctvin1) " \
                  "inner join hosvital.maeemp maeemp on (maeemp.mennit=i.ingnit) inner join hosvital.maemed1 maemed1 on (maemed1.mmusuario = inc.incusureg) inner join hosvital.maeesp esp on (esp.mecode=inc.inccodesp) " \
                  "inner join hosvital.maecaue caue  on (caue.cecodigo= inc.inccaue) where h1.histipdoc='" + tipodoc + "' and h1.hisckey = '" + documento + "' and h1.hiscsec = " + str(folio) + " order by ano"

        cursorInc = con17.cursor()
        cursorInc.execute(comando)
        rowsInc = cursorInc.fetchall()


        if rowsInc == []:
            return localincapacidad
        else:
            for rowInc in rowsInc:
                Story.append(Spacer(1, 3))
                texto1 = 'CERTIFICADO DE INCAPACIDAD'
                Story.append(Paragraph(texto1, headline_mayor))
                Story.append(Spacer(1, 1))
                Story.append(Paragraph(str(rowInc.INCCONPAC), headline_mayor))
                localincapacidad = localincapacidad + 2

                Story.append(Spacer(1, 5))


                tbl_data = [
                    [Paragraph("Nombre:", headline_mayor),
                     Paragraph("", headline_mayor),
                     Paragraph("", headline_mayor),
                     Paragraph("Diagnostico", headline_mayor),
                     Paragraph("Dia", headline_mayor    ),
                     Paragraph("Mes ", headline_mayor),
                     Paragraph("Año ", headline_mayor),
                     Paragraph("", headline_mayor4),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[6 * cm, 1 * cm, 2 * cm, 3 * cm, 2 * cm, 2 * cm, 2 * cm, 1 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph(str(rowInc.NOMBRE), subtitle_atencion),
                     Paragraph(str(rowInc.MPTDOC), subtitle_atencion),
                     Paragraph(str(rowInc.MPCEDU), subtitle_atencion),
                     Paragraph(str(rowInc.HCDXCOD), subtitle_atencion),
                     Paragraph(str(rowInc.DIA), subtitle_atencion),
                     Paragraph(str(rowInc.MES), subtitle_atencion),
                     Paragraph(str(rowInc.ANO), subtitle_atencion),
                     Paragraph("", headline_mayor),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[6 * cm, 1 * cm, 2 * cm, 3 * cm, 2 * cm, 2 * cm, 2 * cm, 1 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Ocupacion:", headline_mayor),
                     Paragraph(str(rowInc.OCUPA), subtitle_atencion),
                     Paragraph("", headline_mayor4),

                     ]]
                tbl1 = Table(tbl_data, colWidths=[8 * cm, 10 * cm, 1 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Empresa:", headline_mayor),
                     Paragraph(str(rowInc.EMPRESA), subtitle_atencion),

                     Paragraph("", headline_mayor4),

                     ]]
                tbl1 = Table(tbl_data, colWidths=[8 * cm, 10 * cm, 1 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Tipo de Incapacidad:", headline_mayor),
                     Paragraph(str(rowInc.TIPO_INCAPACIDAD), subtitle_atencion),
                     Paragraph("Historia clinica:", headline_mayor),
                     Paragraph(str(rowInc.MPCEDU), subtitle_atencion),
                     Paragraph("", headline_mayor4),

                     ]]
                tbl1 = Table(tbl_data, colWidths=[4 * cm, 6 * cm, 4 * cm, 3 * cm, 2 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Fecha Inicia:", headline_mayor),
                     Paragraph(str(rowInc.FECHA_INICIA), subtitle_atencion),
                     Paragraph("Fecha Fin:", headline_mayor),
                     Paragraph(str(rowInc.FECHA_FIN), subtitle_atencion),
                     Paragraph("Dias de Incapacidad o Licencia:", headline_mayor),
                     Paragraph(str(rowInc.DIAS_INCAPACIDAD), subtitle_atencion),
                     Paragraph("", headline_mayor4),

                     ]]
                tbl1 = Table(tbl_data, colWidths=[3 * cm, 3 * cm, 3 * cm, 3 * cm, 5 * cm,1 * cm, 1 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Causa Externa:", headline_mayor),
                     Paragraph(str(rowInc.CAUSA_EXTERNA), subtitle_atencion),
                     Paragraph("Tipo de Atencion::", headline_mayor),
                     Paragraph(str(rowInc.TIPO_ATENCION), subtitle_atencion),
                     Paragraph("Procedimiento:", headline_mayor),
                     Paragraph("", headline_mayor),

                     ]]
                tbl1 = Table(tbl_data, colWidths=[3 * cm, 3 * cm, 4 * cm, 4 * cm, 3 * cm,  2 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Diagnostico relacionador:", headline_mayor),
                     Paragraph("", headline_mayor),
               ]]
                tbl1 = Table(tbl_data, colWidths=[10* cm, 9 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Fecha Accidente Trabajo:", headline_mayor),
                     Paragraph("/ / 00:00:00", subtitle_atencion),
                     Paragraph("Prorroga :", headline_mayor),
                     Paragraph("No", subtitle_atencion),
                     Paragraph("Expedia en:", headline_mayor),
                     Paragraph("FUNDACION HOSPITAL SAN CARLOS", headline_mayor),

                     ]]
                tbl1 = Table(tbl_data, colWidths=[5 * cm, 1.7  * cm,2.2 * cm, 0.7 * cm, 2.5 * cm,7 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Empresa Donde Trabaja:", headline_mayor),
                     Paragraph("", headline_mayor),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[10 * cm, 9 * cm])
                Story.append(tbl1)

                tbl_data = [
                    [Paragraph("Observaciones de Profesional:", headline_mayor),
                     Paragraph("", headline_mayor),
                     ]]
                tbl1 = Table(tbl_data, colWidths=[10 * cm, 9 * cm])
                Story.append(tbl1)


                localincapacidad = localincapacidad + 7
        con17.close()
        localRegistro = self.registro(doc, localincapacidad, Story, tipodoc, documento, folio, headline_mayor,
                                      headline_mayor1,
                                      headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,
                                      subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        return localincapacidad

    def terapiasCancela(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,    subtitle_cabezote, subtitle_nacimiento):

        # Trae Interconsulta
        localTerapiasCan = y
        print("Entre Terapias Cancel Qx Gases No Qx con localTerapiasCan  folio y = ", localTerapiasCan, folio, y)

        con18 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        comando = "select  h1.histipdoc,h1.hisckey,h1.hiscsec folio,h1.hisfhorat as fecha,case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end, " \
                  "h5.hiscpcan cantidad,pro.prnomb as descripcion,  'Cancelado' as Cancelado, case when h51.hcmocntp='1' then 'Admistrativo' when h51.hcmocntp='3' then 'Medico'  end AS MOTIVO_CANCELACION,h51.hcobscan as observaciones,concat(concat(maemed1.mmnomm,'-RM: '), maemed1.mmregm) as usuario_cancela,h51.hcprfhcad as fecha_cancelacion, h5.hiscpobs " \
                  "from hosvital.hccom1 h1 inner join hosvital.hccom5 h5 on (h5.histipdoc=h1.histipdoc and h5.hisckey=h1.hisckey  and h5.hiscsec=h1.hiscsec and h5.hcprctip= 3) " \
                      "inner join hosvital.hccom51 h51 on (h51.histipdoc= h5.histipdoc and h51.hisckey=h5.hisckey and h51.hiscsec=h5.hiscsec and h51.hcprccod= h5.hcprccod and h51.hcprCEST='C') " \
                  "inner join hosvital.maepro pro on (pro.prcodi=h51.hcprccod) left  join hosvital.maemed1 maemed1 on (maemed1.mmusuario=h51.hcpruscad) " \
                  "where  h1.histipdoc='" + tipodoc + "' and h1.hisckey = '" + documento + "' and h1.hiscsec = " + str(
            folio) + " group by h1.histipdoc, h1.hisckey, h1.hiscsec, h1.hisfhorat, h1.hisclpr, h5.hiscpcan, pro.prnomb, 'Cancelado', h51.hcmocntp, h51.hcobscan, concat(concat(maemed1.mmnomm, '-RM: '), maemed1.mmregm), h51.hcprfhcad, h5.hiscpobs"

        cursorTerCan = con18.cursor()
        cursorTerCan.execute(comando)
        rowsTerCan = cursorTerCan.fetchall()

        if rowsTerCan == []:
            return localTerapiasCan
        else:
            localTerapiasCan = localTerapiasCan + 1
            Story.append(Spacer(1, 2))

            texto1 = 'TERAPIAS'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("Descripcion", subtitle_atencion),
                         Paragraph("Estado", subtitle_atencion), ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 10 * cm, 5 * cm])

            localTerapiasCan = localTerapiasCan + 3


            Story.append(tbl1)
            rx = ''
            rx1 = ''
            resul = ''
            resul1 = ''
            for rowTerCan in rowsTerCan:
                rx1 = str(rowTerCan.DESCRIPCION)


                if rx == '' or rx1 != rx:
                    # Story.append(Paragraph(str(rowTerCan.HISCPOBS), subtitle_atencion))
                    tbl_data = [
                        [Paragraph(str(rowTerCan.CANTIDAD), subtitle_atencion),
                         Paragraph(str(rowTerCan.DESCRIPCION), subtitle_atencion),
                         Paragraph(str(rowTerCan.CANCELADO), subtitle_atencion),
                         # Paragraph("", headline_mayor33),
                         ]]
                    localTerapiasCan = localTerapiasCan + 1

                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph("MOTIVO CANCELACION:", headline_mayor2),
                                 Paragraph(str(rowTerCan.MOTIVO_CANCELACION), subtitle_atencion),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 13 * cm, 1 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph("OBSERVACIONES:", headline_mayor2),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[4 * cm, 15 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph(str(rowTerCan.OBSERVACIONES).replace("\n", "<br />"), subtitle_atencion),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[18 * cm, 1 * cm])
                    Story.append(tbl1)

                    Story.append(Spacer(1, 2))


                    tbl_data = [[Paragraph("USUARIO QUE CANCELA:", headline_mayor2),
                                 Paragraph(str(rowTerCan.USUARIO_CANCELA), subtitle_atencion),
                                 Paragraph("", headline_mayor2),]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 13 * cm, 1 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph("FECHA CANCELACION:", headline_mayor2),
                                 Paragraph(str(rowTerCan.FECHA_CANCELACION), subtitle_atencion),
                                 Paragraph("", headline_mayor2),]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 13 * cm, 1 * cm])
                    Story.append(tbl1)
                    Story.append(Spacer(1, 2))
                    rx = rx1

        Story.append(Spacer(1, 1))
        #localRegistro = self.registro(doc, localTerapiasCan, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,     subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        #Story.append(Spacer(1, 1))

        localTerapiasCan = localTerapiasCan + 2
        con18.close()
        return localTerapiasCan

    def QxCancela(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,   subtitle_cabezote, subtitle_nacimiento):

        # Trae Interconsulta
        localQxCan = y
        print("Entre Qx Cancela Cancel Qx Gases No Qx con localQxCan  folio y = ", localQxCan, folio, y)
        con19 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')


        comando = "select h1.histipdoc,h1.hisckey,h1.hiscsec folio,h1.hisfhorat as fecha,case when h1.hisclpr='2' then 'HOSPITALIZACION' when h1.hisclpr='1' then 'AMBULATORIO' when h1.hisclpr='3' then 'URGENCIAS' end SERVICIO, " \
                  "h5.hiscpcan cantidad,pro.prnomb as descripcion,  'Cancelado' as Cancelado, case when h51.hcmocntp='1' then 'Admistrativo' when h51.hcmocntp='3' then 'Medico'  end AS MOTIVO_CANCELACION,h51.hcobscan as observaciones," \
                  "concat(concat(maemed1.mmnomm,'-RM: '), maemed1.mmregm) as usuario_cancela,h51.hcprfhcad as fecha_cancelacion, h5.hiscpobs " \
                  "from hosvital.hccom1 h1 inner join hosvital.hccom5 h5 on (h5.histipdoc=h1.histipdoc and h5.hisckey=h1.hisckey  and h5.hiscsec=h1.hiscsec and h5.hcprctip= 5 ) " \
                  "inner join hosvital.hccom51 h51 on (h51.histipdoc= h5.histipdoc and h51.hisckey=h5.hisckey and h51.hiscsec=h5.hiscsec and h51.hcprccod= h5.hcprccod and h51.hcprCEST='C') " \
                  "inner join hosvital.maepro pro on (pro.prcodi=h51.hcprccod) left join hosvital.maemed1 maemed1 on (maemed1.mmusuario=h51.hcpruscad) " \
                  "where  h1.histipdoc='" + tipodoc + "' and h1.hisckey = '" + documento + "' and h1.hiscsec = " + str(folio) + "  order by pro.prcodi"

        cursorQxCan = con19.cursor()
        cursorQxCan.execute(comando)
        rowsQxCan = cursorQxCan.fetchall()

        if rowsQxCan == []:
            return localQxCan
        else:
            localQxCan = localQxCan + 1



            Story.append(Spacer(1, 2))

            texto1 = 'PROCEDIMIENTOS QUIRURGICOS'
            Story.append(Paragraph(texto1, headline_mayor))
            Story.append(Spacer(1, 1))

            tbl_data = [[Paragraph("Cantidad", subtitle_atencion), Paragraph("Descripcion", subtitle_atencion),
                         Paragraph("Estado", subtitle_atencion), ]]

            tbl1 = Table(tbl_data, colWidths=[4 * cm, 10 * cm, 5 * cm])

            localQxCan = localQxCan + 3
            Story.append(tbl1)
            rx = ''
            rx1 = ''
            resul = ''
            resul1 = ''
            for rowQxCan in rowsQxCan:
                rx1 = str(rowQxCan.DESCRIPCION)

                if rx == '' or rx1 != rx:
                    # Story.append(Paragraph(str(rowQxCan.HISCPOBS), subtitle_atencion))
                    tbl_data = [
                        [Paragraph(str(rowQxCan.CANTIDAD), subtitle_atencion),
                         Paragraph(str(rowQxCan.DESCRIPCION), subtitle_atencion),
                         Paragraph(str(rowQxCan.CANCELADO), subtitle_atencion),
                         # Paragraph("", headline_mayor33),
                         ]]
                    localQxCan = localQxCan + 1

                    tbl1 = Table(tbl_data, colWidths=[1 * cm, 15 * cm, 3 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph("MOTIVO CANCELACION:", headline_mayor2),
                                 Paragraph(str(rowQxCan.MOTIVO_CANCELACION), subtitle_atencion),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 13 * cm, 1 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph("OBSERVACIONES:", headline_mayor2),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[4 * cm, 15 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph(str(rowQxCan.OBSERVACIONES).replace("\n", "<br />"), subtitle_atencion),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[19 * cm, 1 * cm])
                    Story.append(tbl1)

                    Story.append(Spacer(1, 2))

                    tbl_data = [[Paragraph("USUARIO QUE CANCELA:", headline_mayor2),
                                 Paragraph(str(rowQxCan.USUARIO_CANCELA), subtitle_atencion),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 13 * cm, 1 * cm])
                    Story.append(tbl1)

                    tbl_data = [[Paragraph("FECHA CANCELACION:", headline_mayor2),
                                 Paragraph(str(rowQxCan.FECHA_CANCELACION), subtitle_atencion),
                                 Paragraph("", headline_mayor2), ]]

                    tbl1 = Table(tbl_data, colWidths=[5 * cm, 13 * cm, 1 * cm])
                    Story.append(tbl1)
                    Story.append(Spacer(1, 2))
                    rx = rx1

        Story.append(Spacer(1, 1))
        # localRegistro = self.registro(doc, localQxCan, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2, headline_mayor3, headline_mayor33, headline_mayor4,     subtitle_tipoevol, subtitle_atencion, subtitle_cabezote, subtitle_nacimiento)
        # Story.append(Spacer(1, 1))

        localQxCan = localQxCan + 2
        con19.close()
        return localQxCan

def buscapaciente(tipodoc, documento):


    con111 = pyodbc.connect(
        'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

    comando = "select cap.mptdoc tipodoc, cap.mpcedu documento, cap.mpnomc paciente, maeemp.menomb as empresa ,   maetpa3.mtnomp as afiliado, varchar_format(cap.mpfchn ,'dd/mm/yyyy') as fecha_nacimiento , concat((days(current_date) - days(date(cap.mpfchn)))/365, ' AÑOS') as edad_actual, case when cap.mpsexo='M' then 'Masculino'  when cap.mpsexo='F' then 'Femenino' end  as sexo, cap.MPTipAfi	  as grupo_sanguineo,    case when cap.MPEstC= 'C' THEN 'Casado'      when cap.MPEstC= 'S' THEN 'Soltero'  when cap.MPEstC= 'U' THEN 'Union Libre'  when cap.MPEstC= 'V' THEN 'Viudo'  when cap.MPEstC= 'P' THEN ''  when cap.MPEstC= 'O' THEN ''        ELSE ''        end          as estado_civil,     cap.mptele as telefono,cap.mpdire as direccion,   " \
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

    cursor111 = con111.cursor()
    cursor111.execute(comando)
    rows111 = cursor111.fetchall()

    if rows111 == []:

        con111.close()
        return 0
    else:
        con111.close()
        return 1


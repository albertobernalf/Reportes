from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import csv
from django.views.generic import ListView, CreateView, TemplateView, View
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from datetime import date
import pyodbc
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet , ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
import io

import json


class EnvioFacturas(TemplateView):
    print("EnvioFacturas")
    template_name = 'mitemplate2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'
        print("POR QUI PASE INICOP CONTEXTO")

        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST")

        Desde = request.POST.get('Desde', False);
        Hasta = request.POST.get('Hasta', False);
        buff = io.BytesIO()
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="C:\\EntornosPython\\fec\\fec\\prueba.txt"'


        con002 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        cursor002 = con002.cursor()

        comando = "SELECT '860007373' NitFacturador, 'FESC' prefijo, m.mpnfac numeroDocumento, '1' tipoDocumento, '10' tipoOperacion, '01' subTipoDocumento, '1' plantilla, 'true' generaRepresentacionGrafica, m.facfch fechaEmision, " \
         	      "concat(m.facfchhor ,'-05:00') horaEmision,(m.facfch + 30 days) fechaVencimiento,'COP' moneda,1 notif_Tipo, ter.trcemail notif_Valor,'2' as formapago_tipopago, 'ZZZ' formapago_codigomedio,(m.facfch + 30 days) FORMAPAGO_fechaVencimiento, " \
                "'ObservacionesFactura' infoadicional_nombre, 'Factura' infoadicional_valor, substring(maeemp.mecntr, 1, 9) adq_identificacion, case when tipdoc.tipcoddoc = 1 then '31' when tipdoc.tipcoddoc = 2 then '13' when tipdoc.tipcoddoc = 3  then '22' when tipdoc.tipcoddoc = 4 " \
                 "then '12' when tipdoc.tipcoddoc=5 then '11' when tipdoc.tipcoddoc=6 then '41' when tipdoc.tipcoddoc=8 then '11' end  adq_tipoIdentificacion,'669'  adq_codigointerno, '0' adq_matriculamercantil, ter.trcrazsoc adq_razonSocial,  ter.trcrazsoc adq_nombresucursal, " \
                "ter.trcemail adq_correo, ter.trcresfis  adq_responsabilidadesRUT,'1'  adq_tipoPersona, 'CO'  ubi_pais, concat(ter.trcmdcodd ,  lpad(ter.trcmdcodm,3,'0')) ubi_codigoMunicipio,' ' ubi_ciudad, 'departamento' ubi_departamento ,ter.trcdir ubi_direccion,m.matotf tot_valorBruto,'COP' tot_valorBrutoMoneda, m4.afcvlrabo " \
                "tot_valorAnticipo, 'COP' tot_valorantiticipomoneda, m.matotf  tot_valorTotalSinImpuestos,'COP'  tot_SinImpmoneda ,  m.matotf  tot_valorTotalConImpuestos, 'COP'  tot_valorTotalConImpuestosmoneda , m.mavals  tot_valorNeto,'COP' tot_valornetomoneda " \
               "FROM hosvital.maeate m inner join hosvital.maeemp maeemp on (maeemp.mennit =m.mpmeni) inner join hosvital.terceros ter on (ter.trccod=substring(maeemp.mecntr,1,9)) left join hosvital.maeate4 m4 on (m4.mpnfac = m.mpnfac) left join hosvital.tipdoc tipdoc on " \
                  "(tipdoc.tipcoddoc = ter.trctpoide) left join hosvital.tpocont tpocont on (tpocont.tcocod=ter.tcocod ) where m.facfch>= '" + Desde + "' and m.facfch <= '" + Hasta + "' and m.mpmeni <> '90' UNION SELECT '860007373' NitFacturador,'FESC' prefijo,m.mpnfac numeroDocumento, '1' " \
                "tipoDocumento, '10' tipoOperacion , '01' subTipoDocumento,'1' plantilla,'true' generaRepresentacionGrafica, m.facfch fechaEmision,  concat(m.facfchhor ,'-05:00') horaEmision,(m.facfch + 30 days) fechaVencimiento,'COP' moneda,1 notif_Tipo, ter.trcemail notif_Valor, '2' as " \
            "formapago_tipopago, 'ZZZ' formapago_codigomedio, (m.facfch + 30 days) FORMAPAGO_fechaVencimiento,'ObservacionesFactura' infoadicional_nombre,'Factura' infoadicional_valor, m.mpcedu adq_identificacion , case when tipdoc1.tipcoddoc=1 then '31'   when tipdoc1.tipcoddoc=2 then '13' when tipdoc1.tipcoddoc=3 then '22'" \
            "when tipdoc1.tipcoddoc=4 then '12'   when tipdoc1.tipcoddoc=5 then '11' when tipdoc1.tipcoddoc=6 then '41' when tipdoc1.tipcoddoc=8 then '11'   end  adq_tipoIdentificacion,'669'  adq_codigointerno, '0' adq_matriculamercantil, ter.trcrazsoc adq_razonSocial,  ter.trcrazsoc " \
            "adq_nombresucursal,  ter.trcemail adq_correo, ter.trcresfis  adq_responsabilidadesRUT, '1'  adq_tipoPersona,  'CO'  ubi_pais, concat(ter.trcmdcodd ,  lpad(ter.trcmdcodm,3,'0')) ubi_codigoMunicipio,' ' ubi_ciudad, 'departamento' ubi_departamento ,ter.trcdir ubi_direccion, m.matotf tot_valorBruto,'COP' " \
            "tot_valorBrutoMoneda, m4.afcvlrabo tot_valorAnticipo, 'COP' tot_valorantiticipomoneda, m.matotf  tot_valorTotalSinImpuestos, 'COP'  tot_SinImpmoneda ,  m.matotf  tot_valorTotalConImpuestos, 'COP'  tot_valorTotalConImpuestosmoneda , m.mavals  tot_valorNeto,'COP' " \
           "tot_valornetomoneda FROM hosvital.maeate m inner join hosvital.maeemp maeemp on (maeemp.mennit = m.mpmeni) inner join hosvital.terceros ter on (ter.trccod=m.mpcedu) left join hosvital.maeate4 m4 on (m4.mpnfac = m.mpnfac) " \
            "left join hosvital.tipdoc tipdoc on (tipdoc.tipcoddoc = ter.trctpoide) left join hosvital.tpocont tpocont on (tpocont.tcocod=ter.tcocod ) left join hosvital.tipdocasi casi on  (casi.mptdoc = m.mptdoc ) left join hosvital.tipdoc tipdoc1 on ( tipdoc1.tipcoddoc = cast(casi.mptdohom as " \
            "decimal)) where m.facfch>= '" + Desde + "' and m.facfch <= '" + Hasta + "'  and m.mpmeni = '90' order by 3"




        cursor002.execute(comando)
        rows002 = cursor002.fetchall()
        neto= []
        provisional= []
        documento = {}
        adquiriente = {}
        ubicacion = {}
        formapago = {}
        notificaciones = {}
        anticipos = {}
        totales = {}
        Cabezote = {}
        context = {}

        for row002 in rows002:
            #Cabezote["documento"]
            Cabezote = {}
            armado = {}
            notificaciones = {}
            adquiriente = {}
            ubicacion = {}
            formapago = {}
            anticipos = {}
            totales = {}
            adicionales = {}
            documento = {}


            Cabezote["NITFacturador"] = row002.NITFACTURADOR
            Cabezote["prefijo"] = row002.PREFIJO
            Cabezote["numerodocumento"] = str(row002.NUMERODOCUMENTO).replace("Decimal(", "").replace(")", "")
            Cabezote["tipodocumento"] = row002.TIPODOCUMENTO
            Cabezote["tipoOperacion"] = row002.TIPOOPERACION
            Cabezote["subTipoDocumento"] = row002.SUBTIPODOCUMENTO
            Cabezote["plantilla"] = row002.PLANTILLA
            Cabezote["generaRepresentacionGrafica"] = row002.GENERAREPRESENTACIONGRAFICA
            Cabezote["fechaEmision"] = str(row002.FECHAEMISION).replace("datetime.date(", "").replace(")", "")
            Cabezote["horaEmision"] = row002.HORAEMISION
            Cabezote["fechaVencimiento"] = str(row002.FECHAVENCIMIENTO).replace("datetime.date(", "").replace(")", "")
            Cabezote["moneda"] = row002.MONEDA

            notificaciones["tipo"] = row002.NOTIF_TIPO
            notificaciones["valor"] = row002.NOTIF_VALOR

            Cabezote["notificaciones"] = notificaciones

            formapago["tipopago"] = row002.FORMAPAGO_TIPOPAGO
            formapago["codigoMedio"] = row002.FORMAPAGO_CODIGOMEDIO
            formapago["fechaVencimiento"] = str(row002.FORMAPAGO_FECHAVENCIMIENTO).replace("datetime.date(", "").replace(")", "")

            Cabezote["formapago"] = formapago

            adicionales["nombre"] = row002.INFOADICIONAL_NOMBRE
            adicionales["valor"] = row002.INFOADICIONAL_VALOR
            Cabezote["informacionesAdicionales"] = adicionales

            armado["documento"] = Cabezote

            adquiriente["identificacion"] = row002.ADQ_IDENTIFICACION
            adquiriente["tipoIdentificacion"] = row002.ADQ_TIPOIDENTIFICACION
            adquiriente["codigoInterno"] = row002.ADQ_CODIGOINTERNO
            adquiriente["matriculaMercantil"] = row002.ADQ_MATRICULAMERCANTIL
            adquiriente["razonSocial"] = row002.ADQ_RAZONSOCIAL
            adquiriente["nombreSucursal"] = row002.ADQ_NOMBRESUCURSAL
            adquiriente["correo"] = row002.ADQ_CORREO
            adquiriente["responsabilidadesRUT"] = row002.ADQ_RESPONSABILIDADESRUT
            adquiriente["tipoPersona"] = row002.ADQ_TIPOPERSONA

            ubicacion["pais"] = row002.UBI_PAIS
            ubicacion["codigoMunicipio"] = row002.UBI_CODIGOMUNICIPIO
            ubicacion["ciudad"] = row002.UBI_CIUDAD
            ubicacion["departamento"] = row002.UBI_DEPARTAMENTO
            ubicacion["direccion"] = row002.UBI_DIRECCION

            adquiriente["ubicacion"] = ubicacion

            armado["adquiriente"] = adquiriente

            totales["valorBruto"] = str(row002.TOT_VALORBRUTO).replace("Decimal(", "").replace(")", "")
            totales["valorBrutoMoneda"] = str(row002.TOT_VALORBRUTOMONEDA)
            totales["valorAnticipos"] = str(row002.TOT_VALORANTICIPO).replace("Decimal(", "").replace(")", "")
            totales["valorAnticiposMoneda"] = str(row002.TOT_VALORANTITICIPOMONEDA)
            totales["valorTotalSinImpuestos"] = str(row002.TOT_VALORTOTALSINIMPUESTOS).replace("Decimal(", "").replace(")", "")
            totales["valorTotalSinImpuestosMoneda"] = str(row002.TOT_SINIMPMONEDA)
            totales["valorTotalConImpuestos"] = str(row002.TOT_VALORTOTALCONIMPUESTOS).replace("Decimal(", "").replace(")", "")
            totales["valorTotalConImpuestosMoneda"] = str(row002.TOT_VALORTOTALCONIMPUESTOSMONEDA)
            totales["valorNeto"] = str(row002.TOT_VALORNETO).replace("Decimal(", "").replace(")", "")
            totales["valorNetoMoneda"] = str(row002.TOT_VALORNETOMONEDA)
            armado["totales"] = totales


            #neto.append(armado)
            #str(neto).replace("[{", "").replace("}]","")



            #con002.close()



            context['neto'] = neto

            f = open('C:\\EntornosPython\\fec\\fec\\prueba.txt', "w")
            f.write(str(neto))
            f.close()

        # Segunda parte el detalle

            print("IMPRIMI CABEZOTE FACTURA : ", str(row002.NUMERODOCUMENTO).replace("Decimal(", "").replace(")", "") )

            con022 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

            cursor022 = con022.cursor()
            comando = "SELECT  m.mpnfac, m2.macscp consec,'1' as det_tipoDetalle, m2.prcodi valorCodigoInterno, '999' codigoestandar,m2.prcodi valorCodigoEstandar, '04' unidadMedida, maepro.prnomb descripcion,m2.macanpr  unidades, m2.mpinte valorUnitarioBruto,   'COP' " \
                      "valorunitariobrutomoneda,   m2.mavatp valorBruto,    'COP' valorBrutoMoneda,'1' tipodetalle,'Codigo' infadicnombre,'999' infadicvalor FROM hosvital.maeate m inner join hosvital.maeate2 m2 on (m2.mpnfac=m.mpnfac and m2.fcptpotrn='F' and m2.maesanup<>'S') " \
                     "inner join hosvital.maepro maepro on (maepro.prcodi=m2.prcodi) WHERE  m.mpnfac = " + str(row002.NUMERODOCUMENTO).replace("Decimal(", "").replace(")", "")  + " union SELECT  m.mpnfac, m3.macscs consec,'1' as det_tipoDetalle, m3.msreso " \
                      "valorCodigoInterno, '999' codigoestandar,m3.msreso valorCodigoEstandar, '04' unidadMedida,   maesum1.msnomg descripcion, m3.macans  unidades, m3.mavalu valorUnitarioBruto,   'COP' valorunitariobrutomoneda,        m3.mavats valorBruto, 'COP' valorBrutoMoneda,'1' " \
                    "tipodetalle,'Codigo' infadicnombre,'999' infadicvalor FROM hosvital.maeate m inner join hosvital.maeate3 m3 on (m3.mpnfac=m.mpnfac and m3.fcstpotrn='F' and m3.maesanus<>'S') inner join hosvital.maesum1 maesum1 on (maesum1.msreso=m3.msreso) WHERE " \
                     " m.mpnfac = " + str(row002.NUMERODOCUMENTO).replace("Decimal(", "").replace(")", "")  + "  order by  1,2"


            cursor022.execute(comando)
            rows022 = cursor022.fetchall()

            detalle = {}
            adicionales = {}
            provisional = []
          
            for row022 in rows022:

              detalle = {}
              adicionales = {}


              detalle["valorCodigoInterno"] = row022.VALORCODIGOINTERNO
              detalle["codigoEstandar"] = row022.CODIGOESTANDAR
              detalle["valorCodigoEstandar"] = row022.VALORCODIGOESTANDAR
              detalle["unidadMedida"] = row022.UNIDADMEDIDA
              detalle["descripcion"] = row022.DESCRIPCION
              detalle["unidades"] = str(row022.UNIDADES).replace("Decimal(", "").replace(")", "")
              detalle["valorUnitarioBruto"] = str(row022.VALORUNITARIOBRUTO).replace("Decimal(", "").replace(")", "")
              detalle["valorUnitarioBrutoMoneda"] = row022.VALORUNITARIOBRUTOMONEDA
              detalle["valorBruto"] = str(row022.VALORBRUTO).replace("Decimal(", "").replace(")", "")
              detalle["valorBrutoMoneda"] = str(row022.VALORBRUTOMONEDA)
              detalle["tipoDetalle"] = str(row022.TIPODETALLE)

              adicionales["nombre"] = str(row022.INFADICNOMBRE)
              adicionales["valor"] = str(row022.INFADICVALOR)

              detalle["informacionesAdicionales"] = adicionales
              provisional.append(detalle)


            armado["detalles"] = provisional
            neto.append(armado)
            con022.close()
            print("IMPRIMI detalle FACTURA : ", str(row002.NUMERODOCUMENTO).replace("Decimal(", "").replace(")", ""))

        con002.close()



        context['neto'] = neto


        f = open('C:\\EntornosPython\\fec\\fec\\pruebaFinal.txt', "w")
        f.write(str(neto))
        f.close()
        # Fin segunda parte

        #return response

        return render(request, "mitemplate2.html", context)




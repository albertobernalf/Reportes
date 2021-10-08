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
        comando = "SELECT '860007373' NitFacturador,'FESC' prefijo,m.mpnfac numeroDocumento,  '1'   tipoDocumento, '01' subTipoDocumento,'true' generaRepresentacionGrafica, m.facfch fechaEmision, m.facfchhor  horaEmision,'COP' " \
                  "moneda,'Empresa' unidadNegocio,'SS-CUFE' tipoOperacion, '1' Plantilla,1 notif_Tipo, ter.trcemail notif_Valor,'1' as pago_tipopago, '10' pago_codigomedio,(m.facfch + 30 days) pago_fechaVencimiento, " \
                   "substring(maeemp.mecntr,1,9) adq_identificacion , case when tipdoc.tipcoddoc=1 then '31'   when tipdoc.tipcoddoc=2 then '13' when tipdoc.tipcoddoc=3 then '22'   when tipdoc.tipcoddoc=4 then '12' when " \
                 "tipdoc.tipcoddoc=5 then '11' when tipdoc.tipcoddoc=6 then '41' when tipdoc.tipcoddoc=8 then '11'   end  adq_tipoIdentificacion, ter.trcrazsoc adq_razonSocial,  ter.trcemail adq_correo, " \
                    "'1'  adq_tipoPersona,   ter.trcrazsoc adq_nombreSucursal, ter.trcresfis  adq_responsabilidadesRUT,  'CO'  ubi_pais, ter.trcmdcodd ubi_codigoMunicipio, ter.trcdir ubi_direccion, " \
                    "m4.abonum  ant_comprobante, m4.afcvlrabo ant_valorAnticipo, 'COP' ant_valorAnticipoMoneda,m.matotf tot_valorBruto, m.mavaab tot_valorAnticipos, m.matotf tot_valorTotalSinImpuestos,  m.matotf " \
                   "tot_valorTotalConImpuestos, m.mavals  tot_valorNeto FROM hosvital.maeate m inner join hosvital.maeemp maeemp on (maeemp.mennit = m.mpmeni) inner join hosvital.terceros ter on (ter.trccod=substring(maeemp.mecntr,1,9)) " \
                    "left join hosvital.maeate4 m4 on (m4.mpnfac = m.mpnfac) left join hosvital.tipdoc tipdoc on (tipdoc.tipcoddoc = ter.trctpoide) left join hosvital.tpocont tpocont on (tpocont.tcocod=ter.tcocod )  " \
                    "where m.facfch >= '" + Desde + "' and m.facfch <= '" + Hasta + "' and m.mpmeni <> '90' UNION SELECT '860007373' NitFacturador,'FESC' prefijo,m.mpnfac numeroDocumento,  '1' tipoDocumento, '01' subTipoDocumento,'true' " \
                    "generaRepresentacionGrafica, m.facfch fechaEmision, m.facfchhor  horaEmision,'COP' moneda, 'Empresa' unidadNegocio,'SS-CUFE' tipoOperacion, '1' Plantilla,1 notif_Tipo, ter.trcemail notif_Valor,'1' as pago_tipopago, '10'  " \
                    "pago_codigomedio,(m.facfch + 30 days) pago_fechaVencimiento, m.mpcedu adq_identificacion , case when tipdoc1.tipcoddoc=1 then '31'   when tipdoc1.tipcoddoc=2 then '13' when tipdoc1.tipcoddoc=3 then '22'   when  " \
                 "tipdoc1.tipcoddoc=4 then '12'   when tipdoc1.tipcoddoc=5 then '11' when tipdoc1.tipcoddoc=6 then '41' when tipdoc1.tipcoddoc=8 then '11'   end  adq_tipoIdentificacion, ter.trcrazsoc adq_razonSocial, " \
                 "ter.trcemail adq_correo,  '2'  adq_tipoPersona,   ter.trcrazsoc adq_nombreSucursal, ter.trcresfis  adq_responsabilidadesRUT,  'CO'  ubi_pais, ter.trcmdcodd ubi_codigoMunicipio, ter.trcdir ubi_direccion, " \
                "m4.abonum ant_comprobante, m4.afcvlrabo ant_valorAnticipo, 'COP'  ant_valorAnticipoMoneda,m.matotf tot_valorBruto,m.mavaab tot_valorAnticipos, m.matotf tot_valorTotalSinImpuestos,m.matotf  tot_valorTotalConImpuestos, " \
                "m.mavals  tot_valorNeto   FROM hosvital.maeate m inner join hosvital.maeemp maeemp on (maeemp.mennit = m.mpmeni) inner join hosvital.terceros ter on (ter.trccod=m.mpcedu) " \
                "left join hosvital.maeate4 m4 on (m4.mpnfac = m.mpnfac) left join hosvital.tipdoc tipdoc on (tipdoc.tipcoddoc = ter.trctpoide) " \
                    "left join hosvital.tpocont tpocont on (tpocont.tcocod=ter.tcocod ) left join hosvital.tipdocasi casi on  (casi.mptdoc = m.mptdoc ) " \
                    "left join hosvital.tipdoc tipdoc1 on ( tipdoc1.tipcoddoc = cast(casi.mptdohom as decimal)) where m.facfch >= '" + Desde + "' and m.facfch <= '" + Hasta + "' order by 3"

        cursor002.execute(comando)
        rows002 = cursor002.fetchall()
        neto= []
        documento = {}
        adquiriente = {}
        ubicacion = {}
        formapago = {}
        notificaciones = {}
        anticipos = {}
        totales = {}
        Cabezote = {}

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
            documento = {}


            Cabezote["NITFacturador"] = row002.NITFACTURADOR
            Cabezote["prefijo"] = row002.PREFIJO
            Cabezote["numerodocumento"] = str(row002.NUMERODOCUMENTO).replace("Decimal(", "").replace(")", "")
            Cabezote["tipodocumento"] = row002.TIPODOCUMENTO
            Cabezote["subTipoDocumento"] = row002.SUBTIPODOCUMENTO
            Cabezote["generaRepresentacionGrafica"] = row002.GENERAREPRESENTACIONGRAFICA
            Cabezote["fechaEmision"] = str(row002.FECHAEMISION).replace("datetime.date(", "").replace(")", "")
            Cabezote["horaEmision"] = row002.HORAEMISION
            Cabezote["moneda"] = row002.MONEDA
            Cabezote["unidadNegocio"] = row002.UNIDADNEGOCIO
            Cabezote["tipoOperacion"] = row002.TIPOOPERACION
            Cabezote["plantilla"] = row002.PLANTILLA

            notificaciones["tipo"] = row002.NOTIF_TIPO
            notificaciones["valor"] = row002.NOTIF_VALOR

            Cabezote["notificaciones"] = notificaciones

            formapago["tipopago"] = row002.PAGO_TIPOPAGO
            formapago["codigoMedio"] = row002.PAGO_CODIGOMEDIO
            formapago["fechaVencimiento"] = str(row002.PAGO_FECHAVENCIMIENTO).replace("datetime.date(", "").replace(")", "")

            Cabezote["formapago"] = formapago

            armado["documento"] = Cabezote

            adquiriente["identificacion"] = row002.ADQ_IDENTIFICACION
            adquiriente["tipoIdentificacion"] = row002.ADQ_TIPOIDENTIFICACION
            adquiriente["razonSocial"] = row002.ADQ_RAZONSOCIAL
            adquiriente["correo"] = row002.ADQ_CORREO
            adquiriente["tipoPersona"] = row002.ADQ_TIPOPERSONA
            adquiriente["nombreSucursal"] = row002.ADQ_NOMBRESUCURSAL
            adquiriente["responsabilidadesRUT"] = row002.ADQ_RESPONSABILIDADESRUT

            ubicacion["pais"] = row002.UBI_PAIS
            ubicacion["codigoMunicipio"] = row002.UBI_CODIGOMUNICIPIO
            ubicacion["direccion"] = row002.UBI_DIRECCION

            adquiriente["ubicacion"] = ubicacion

            armado["adquiriente"] = adquiriente



            anticipos["comprobante"] = row002.ANT_COMPROBANTE
            anticipos["valorAnticipo"] = str(row002.ANT_VALORANTICIPO).replace("Decimal(", "").replace(")", "")
            anticipos["valorAnticipoMoneda"] = row002.ANT_VALORANTICIPOMONEDA

            armado["anticipos"] = anticipos

            totales["valorBruto"] = str(row002.TOT_VALORBRUTO).replace("Decimal(", "").replace(")", "")
            totales["valorAnticipos"] = str(row002.TOT_VALORANTICIPOS).replace("Decimal(", "").replace(")", "")
            totales["valorTotalSinImpuestos"] = str(row002.TOT_VALORTOTALSINIMPUESTOS).replace("Decimal(", "").replace(")", "")
            totales["valorTotalConImpuestos"] = str(row002.TOT_VALORTOTALCONIMPUESTOS).replace("Decimal(", "").replace(")", "")
            totales["valorNeto"] = str(row002.TOT_VALORNETO).replace("Decimal(", "").replace(")", "")

            armado["totales"] = totales


            neto.append(armado)
            #str(neto).replace("[{", "").replace("}]","")


        print(Cabezote)
        print(neto)
        con002.close()

        context = {}
        context['Cabezote'] = Cabezote
        context['neto'] = neto

        f = open('C:\\EntornosPython\\fec\\fec\\prueba.txt', "w")
        f.write(str(neto))
        f.close()

        # Segunda parte el detalle

        con022 = pyodbc.connect(
            'DRIVER=iSeries Access ODBC Driver;SYSTEM=192.168.0.185;UID=abernal;PWD=750222;DBQ=hosvital;EXTCOLINFO=1')

        cursor022 = con022.cursor()
        comando = "SELECT  m.mpnfac, m2.macscp consec,'1' as det_tipoDetalle, m2.prcodi det_valorCodigoInterno, maepro.prnomb det_descripcion,m2.macanpr  det_unidades, m2.mpinte det_valorUnitarioBruto, m2.mavatp det_valorBruto, " \
                  " 'COP' det_valorBrutoMoneda, '999' det_codigoEstandar, '04' det_unidadMedida,m2.prcodi det_valorCodigoEstandar, '01' det_tributos_id,  '01' det_tributos_nombre,  'true' det_tributos_esImpuesto, 0.00 det_tributos_valorImporte " \
                  " , m2.mavatp det_tributos_valorBase,  0.00 det_tributos_porcentaje FROM hosvital.maeate m inner join hosvital.maeate2 m2 on (m2.mpnfac=m.mpnfac and m2.fcptpotrn='F' and m2.maesanup<>'S') " \
                "inner join hosvital.maepro maepro on (maepro.prcodi=m2.prcodi) WHERE  m.facfch >= '" + Desde + "' and m.facfch <= '" + Hasta + "' UNION " \
                " SELECT m.mpnfac ,  m3.macscs consec,'1' as det_tipoDetalle, m3.msreso det_valorCodigoInterno, maesum1.msnomg det_descripcion,m3.macans  det_unidades, m3.mavalu det_valorUnitarioBruto, m3.mavats det_valorBruto," \
                " 'COP' det_valorBrutoMoneda, '999' det_codigoEstandar, '04' det_unidadMedida, m3.msreso det_valorCodigoEstandar, '01' det_tributos_id,  '01' det_tributos_nombre,  'true' det_tributos_esImpuesto,  0.00 det_tributos_valorImporte ," \
                "m3.mavats det_tributos_valorBase, 0.00 det_tributos_porcentaje FROM hosvital.maeate m inner join hosvital.maeate3 m3 on (m3.mpnfac=m.mpnfac and m3.fcstpotrn='F' and m3.maesanus<>'S') inner join hosvital.maesum1 maesum1 on " \
                "(maesum1.msreso=m3.msreso) WHERE  m.facfch >= '" + Desde + "' and m.facfch <= '" + Hasta + "' order by  1,2"

        cursor022.execute(comando)
        rows022 = cursor022.fetchall()
        netoDetalle = []
        detalle = {}
        tributos = {}


        for row022 in rows022:

            detalle = {}
            tributos = {}

            detalle["tipoDetalle"] = row022.DET_TIPODETALLE
            detalle["valorCodigoInterno"] = row022.DET_VALORCODIGOINTERNO
            detalle["descripcion"] = row022.DET_DESCRIPCION
            detalle["unidades"] = str(row022.DET_UNIDADES).replace("Decimal(", "").replace(")", "")
            detalle["valorUnitarioBruto"] = str(row022.DET_VALORUNITARIOBRUTO).replace("Decimal(", "").replace(")", "")
            detalle["valorBruto"] = str(row022.DET_VALORBRUTO).replace("Decimal(", "").replace(")", "")
            detalle["valorBrutoMoneda"] = str(row022.DET_VALORBRUTOMONEDA).replace("Decimal(", "").replace(")", "")
            detalle["codigoEstandar"] = row022.DET_CODIGOESTANDAR
            detalle["unidadMedida"] = row022.DET_UNIDADMEDIDA
            detalle["valorCodigoEstandar"] = row022.DET_VALORCODIGOESTANDAR

            tributos["id"] = row022.DET_TRIBUTOS_ID
            tributos["nombre"] = row022.DET_TRIBUTOS_NOMBRE
            tributos["esImpuesto"] = row022.DET_TRIBUTOS_ESIMPUESTO
            tributos["valorImporte"] = str(row022.DET_TRIBUTOS_VALORIMPORTE).replace("Decimal(", "").replace(")", "")
            tributos["valorBase"] = str(row022.DET_TRIBUTOS_VALORBASE).replace("Decimal(", "").replace(")", "")
            tributos["porcentaje"] = str(row022.DET_TRIBUTOS_PORCENTAJE).replace("Decimal(", "").replace(")", "")

            detalle["tributos"] =tributos




            netoDetalle.append(detalle)

        print(netoDetalle)

        con022.close()


        context['Cabezote'] = Cabezote
        context['neto'] = neto
        context['netoDetalle'] = netoDetalle

        f = open('C:\\EntornosPython\\fec\\fec\\prueba1.txt', "w")
        f.write(str(netoDetalle))
        f.close()
        # Fin segunda parte

        #return response

        return render(request, "mitemplate2.html", context)




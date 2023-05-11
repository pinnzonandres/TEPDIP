import pandas as pd
from openpyxl.styles import PatternFill
from datetime import datetime
import os

month_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 
              4: 'Abril', 5: 'Mayo', 6: 'Junio', 
              7: 'Julio', 8: 'Agosto', 9: 'Septiembre',
              10: 'Octubre', 11: 'Noviembre', 12:'Diciembre'}

def datos_excel(dataframe):
    dataframe.loc['TOTAL'] = [''] + dataframe.iloc[:,1:].sum().tolist()
    dataframe.loc['TOTAL','RUBRO'] = 'TOTAL DIP'
    dataframe.loc['TOTAL','DESCRIPCION'] = 'TOTAL DIP'
    dataframe.loc['TOTAL','% COMPROMETIDO (B/A)'] = round((dataframe.loc['TOTAL','COMPROMISO (B)'] / dataframe.loc['TOTAL','APR. VIGENTE (A)']), 4)
    dataframe.loc['TOTAL','% EJECUCIÓN (C/A)'] = round((dataframe.loc['TOTAL','PAGOS (C)'] / dataframe.loc['TOTAL','APR. VIGENTE (A)']), 4)
    
    return dataframe

def ctr_reservas(dataframe):
    reserva_DIP = dataframe[dataframe['Dirección'] == 'Inclusión Productiva'].reset_index(drop=True)
    total_reserva = reserva_DIP['Valor Actual'].sum()
    
    reserva_DIP = reserva_DIP[['Descripción Rubro','Numero Documento Soporte','Nombre Razon Social','Valor Actual','Valor Obligaciones','Valor Ordenes de Pago']]
    reserva_DIP = reserva_DIP.rename(columns={'Descripción Rubro':'PROGRAMA',
                                            'Numero Documento Soporte':'CONVENIO / CONTRATO',
                                            'Nombre Razon Social': 'TERCERO',
                                            'Valor Actual':'VALOR CONSTITUCION DE RESERVA',
                                            'Valor Obligaciones':'OBLIGADO',
                                            'Valor Ordenes de Pago':'PAGADO'})
    
    data = {}
    result = pd.DataFrame()
    for i in set(reserva_DIP['PROGRAMA'].values):
        data[i] = reserva_DIP[reserva_DIP['PROGRAMA']==i]
        data[i] = data[i].groupby('CONVENIO / CONTRATO').agg({'PROGRAMA':'first',
                                                            'TERCERO':'first',
                                                            'VALOR CONSTITUCION DE RESERVA':'sum',
                                                            'OBLIGADO':'sum',
                                                            'PAGADO':'sum'}).reset_index(drop = False)
        data[i] = data[i][data[i]['VALOR CONSTITUCION DE RESERVA']!=0].reset_index(drop = True)
        data[i]['% DE RESERVA'] = data[i].apply(lambda x: round(int(x['VALOR CONSTITUCION DE RESERVA'])/ int(total_reserva) ,2), axis = 1) 
        data[i]['% EJECUCION'] = data[i].apply(lambda x: round(int(x['PAGADO']) / int(x['VALOR CONSTITUCION DE RESERVA']), 2), axis = 1)
        data[i] = data[i][['PROGRAMA','CONVENIO / CONTRATO','TERCERO','VALOR CONSTITUCION DE RESERVA','% DE RESERVA','OBLIGADO','PAGADO','% EJECUCION']]
        data[i].loc['TOTAL'] = [''] + data[i].iloc[:,1:].sum().tolist()
        data[i].loc['TOTAL','PROGRAMA'] = f'Total {i}'
        data[i].loc['TOTAL','CONVENIO / CONTRATO'] = ''
        data[i].loc['TOTAL','TERCERO'] = ''
        data[i].loc['TOTAL','% DE RESERVA'] = round(int(data[i].loc['TOTAL','VALOR CONSTITUCION DE RESERVA']) / int(total_reserva), 4)
        data[i].loc['TOTAL','% EJECUCION'] = round(int(data[i].loc['TOTAL','PAGADO']) / int(data[i].loc['TOTAL','VALOR CONSTITUCION DE RESERVA']), 4)
        
        result = pd.concat([result,data[i]])       

    result.loc['TOTAL RESERVAS','PROGRAMA'] = 'TOTAL RESERVAS DIP'
    result.loc['TOTAL RESERVAS','VALOR CONSTITUCION DE RESERVA'] = reserva_DIP['VALOR CONSTITUCION DE RESERVA'].sum()
    result.loc['TOTAL RESERVAS','% DE RESERVA'] = 1
    result.loc['TOTAL RESERVAS','OBLIGADO'] = reserva_DIP['OBLIGADO'].sum()
    result.loc['TOTAL RESERVAS','PAGADO'] = reserva_DIP['PAGADO'].sum()
    result.loc['TOTAL RESERVAS','% EJECUCION'] = round(int(result.loc['TOTAL RESERVAS','PAGADO']) / int(result.loc['TOTAL RESERVAS','VALOR CONSTITUCION DE RESERVA']), 2)
    return result

def export_report(archivo_de_datos, path, month, year):
    path_file = os.path.join(path,'Ejec Pptal '+ month_dict[month] + ' 2023.xlsx')
    writer = pd.ExcelWriter(path_file, engine='openpyxl')

# Convertir el DataFrame en una hoja de Excel
    archivo_de_datos['RG_Excel'].to_excel(writer, sheet_name='Ejecución Pptal Agregada DIP', index=False, startrow=3)

    # Obtener la hoja de Excel
    workbook = writer.book
    hoja = writer.sheets['Ejecución Pptal Agregada DIP']

    # Agregar el formato de tabla
    #hoja.add_table(hoja.dimensions)

    # Agregar los valores a las celdas
    hoja['A1'] = 'Año fiscal:'
    hoja['B1'] = year
    hoja['A2'] = 'Vigencia:'
    hoja['B2'] = 'Actual'
    hoja['A3'] = 'Periodo:'
    hoja['B3'] = month_dict[month]


    archivo_de_datos['Reservas_Excel'].to_excel(writer, sheet_name='Control RVAS', index=False, startrow=1)
    hoja2 = writer.sheets['Control RVAS']

    light_blue_fill = PatternFill(start_color='E6F3FF', end_color='E6F3FF', fill_type='solid')
        
    for row in hoja2.iter_rows():
        if 'Total' in str(row[0].value):
            for cell in row:
                cell.fill = light_blue_fill
                
    # Guardar el archivo
    writer.close()
    


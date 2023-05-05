import pandas as pd

## Diccionarios para añadir el mes de cada fila
month_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 
              4: 'Abril', 5: 'Mayo', 6: 'Junio', 
              7: 'Julio', 8: 'Agosto', 9: 'Septiembre',
              10: 'Octubre', 11: 'Noviembre', 12:'Diciembre'} 

# Lista de Meses
month_list = ['Enero','Febrero','Marzo', 
              'Abril','Mayo','Junio', 
              'Julio','Agosto','Septiembre',
              'Octubre','Noviembre','Diciembre']

dict_month = {'Enero':1,'Febrero':2,'Marzo':3, 
              'Abril':4,'Mayo':5,'Junio':6, 
              'Julio':7,'Agosto':8,'Septiembre':9,
              'Octubre':10,'Noviembre':11,'Diciembre':12}

## Funcion para añadir el mes
def _month_add(data, col):
    data[col] = pd.to_datetime(data[col])
    data['No. Mes'] = data.apply(lambda x: x[col].month, axis = 1)
    data['Mes'] = data.apply(lambda x: month_dict[int(x['No. Mes'])], axis = 1)
    
    return data

def get_fourth_base(RP, OP, month):
    OP = OP[OP['Estado']=='Pagada'].reset_index(drop = True)
    
    GRP = RP.groupby(by = ['Compromisos','Index_Rubro','Recurso']).agg({'Fecha de Creacion':'first',
                                                         'Estado':'first',
                                                         'Dependencia' : 'first',
                                                        'Dependencia Descripcion':'first',
                                                         'Fuente' : 'first',
                                                         'Valor Inicial': 'sum',
                                                         'Valor Operaciones': 'sum',
                                                         'Valor Actual': 'sum',
                                                         'Saldo por Utilizar':'sum',
                                                         'Tipo Identificacion': 'first',
                                                         'Nombre Razon Social': 'first',
                                                         'CDP':'first',
                                                         'Obligaciones':'first',
                                                         'Ordenes de Pago' : 'first',
                                                         'Fecha Documento Soporte': 'first',
                                                         'Tipo Documento Soporte': 'first',
                                                         'Numero Documento Soporte' : 'first',
                                                         'Observaciones': 'first',
                                                         'Descripción Rubro':'first',
                                                         'Dirección':'first'}).reset_index(drop = False)
    
    ## Añadimos el mes a la base GRP
    GRP = _month_add(GRP, 'Fecha de Creacion')

    ## Añadimos la columna de Tipo de Contratista
    GRP['Tipo Contratista'] = GRP['Tipo Identificacion'].apply(lambda x: 'Persona natural' if x =='Cédula de Ciudadanía' else 'Persona jurídica')
    
    ## Añadimos las columnas de mes a la base OP
    MOP = _month_add(OP, 'Fecha de pago')
    
    # Agrupamos la base MOP por las columnas necesarias para el merge
    GOP = MOP.groupby(by = ['Compromisos','Index_Rubro','No. Mes','Recurso']).agg({'Fecha de Registro':'first',
                                                        'Fecha de pago':'first',
                                                        'Valor Neto Pesos':'sum',
                                                        'Mes':'first'}).reset_index(drop = False)
    GOP = GOP.rename(columns = {'Valor Neto Pesos' : 'Valor Ordenes de Pago'})
    
    Comp_Rubro ={i:list(set(list(set(GRP[GRP['Compromisos']==i]['Index_Rubro'].values)))) for i in list(set(GRP['Compromisos'].values))}
    
    result = pd.DataFrame()
    result = pd.concat([result, GRP], ignore_index = True)
    for i in Comp_Rubro:
        for j in Comp_Rubro[i]:
            df = GRP[(GRP['Compromisos']== i) & (GRP['Index_Rubro']== j )]
            faltantes = month_list[df['No. Mes'][df.index[0]]:month]
            for n in faltantes:
                data = df
                data.loc[data.index,'No. Mes'] = dict_month[n]
                data.loc[data.index,'Mes'] = n
                result = pd.concat([result, data], ignore_index = True)
                
    GR = result.merge(GOP, how = 'left', on = ['Compromisos', 'Index_Rubro','No. Mes','Mes','Recurso'])
    GR['Valor Ordenes de Pago'].fillna(0, inplace = True)
    GR = GR.sort_values('No. Mes' , ascending = True, ignore_index = True)
    GR['Valor Neto Acumulado'] = GR.groupby(by =['Compromisos','Index_Rubro','Recurso'])['Valor Ordenes de Pago'].cumsum()
    
    return GR
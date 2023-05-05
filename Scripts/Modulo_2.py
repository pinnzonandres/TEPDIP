import pandas as pd

## Diccionarios para añadir el mes de cada fila
month_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 
              4: 'Abril', 5: 'Mayo', 6: 'Junio', 
              7: 'Julio', 8: 'Agosto', 9: 'Septiembre',
              10: 'Octubre', 11: 'Noviembre', 12:'Diciembre'} 

## Función para añdir los meses y su respectivo No. Mes
def _month_add(data, col):
    data[col] = pd.to_datetime(data[col])
    data['No. Mes'] = data.apply(lambda x: x[col].month, axis = 1)
    data['Mes'] = data.apply(lambda x: month_dict[int(x['No. Mes'])], axis = 1)
    
    return data

def agrupar_mes(data, valor, Nombre_columna):
    
    gr = data.groupby(by=['Index_Rubro','Mes','Recurso']).agg({valor:'sum',
                                                     'Dirección':'first',
                                                     'Descripción Rubro': 'first',
                                                     'No. Mes': 'first'}).reset_index(drop = False)
    gr = gr.rename(columns={valor : Nombre_columna})
    
    return gr

def get_pre_second_base(RG, CDP, RP, OB, OP, month):
    
    ## Seleccionamos las columnas que necesitamos unicamente del valor inicial
    GENERAL = RG.iloc[:,[0,1,2,3,7]]
    
    ## Creamos un dataframe donde guardamos la información del dataframe original para cada mes
    result = pd.DataFrame()
    for i in month_dict.keys():
        if i <= month:
            df = GENERAL
            df.loc[:, 'No. Mes'] = i
            df.loc[:,'Mes'] = month_dict[i]
            result = pd.concat([result,df]).reset_index(drop=True)
            
    ## Filtramos las ordenes de pago solo por aquellas que ya están pagadas para quitar las únicamente creadas
    OP = OP[OP['Estado']=='Pagada'].reset_index(drop = True)
    
    ### Añadimos la columna de mes para cada base de datos
    CDP = _month_add(CDP, 'Fecha de Creacion')
    RP = _month_add(RP, 'Fecha de Creacion')
    OB = _month_add(OB, 'Fecha de Creacion')
    OP = _month_add(OP, 'Fecha de pago')
    
    ## Agrupamos nuestros datos para tener la información agrupada por cada uno de los meses en la columna preestablecida
    GCDP = agrupar_mes(CDP, 'Valor Actual', 'Valor CDP')
    GRP = agrupar_mes(RP, 'Valor Actual', 'Valor RP')
    GOB = agrupar_mes(OB, 'Valor Actual.1', 'Valor OB')
    GOP = agrupar_mes(OP, 'Valor Neto Pesos', 'Valor OP')
    
    ## Añadimos cada columna a nuestra base de datos
    result = result.merge(GCDP, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result = result.merge(GRP, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result = result.merge(GOB, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result = result.merge(GOP, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result.fillna(0, inplace = True)
    
    
    ## Hacemos la suma acumulada para tener el resultado acumulado por cada mes
    result['CDP Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor CDP'].cumsum(numeric_only=True)
    result['RP Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor RP'].cumsum(numeric_only=True)
    result['OB Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor OB'].cumsum(numeric_only=True)
    result['OP Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor OP'].cumsum(numeric_only=True)
    
    return result

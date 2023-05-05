import pandas as pd

# Función para poder cambiar todas las columnas númericas de tipo texto a su valor númerico
def str_to_float(data, columnas):
    for i in columnas:
        data[i] = data[i].apply(lambda x: float(str(x).replace(",","")))
    return data

# Función para concatenar las bases de datos 
def unificar_data(data1, data2):
    
    ## Eliminamos aquellas columnas vacias que no tienen información
    data1 = data1.dropna(subset=data1.columns[0]).reset_index(drop = True)
    data2 = data2.dropna(subset=data2.columns[0]).reset_index(drop = True)
    
    ## Creamos las listas y el diccionario necesario para que los datasets tengan las mismas columnas
    n_data1 = list(data1.columns)
    n_data2 = list(data2.columns)
    names = {n_data2[i]:n_data1[i] for i in range(len(n_data1))}
    
    data2 = data2.rename(columns = names)
    
    # Concatenamos las bases de datos
    result = pd.concat([data1, data2]).reset_index(drop = True)
    
    return result

# Función para filtrar por los rubros de la DIP y añadir su respectiva descripción
## Diccionario de descripcion
rubro_names = {'13':"ReSA",
               '14':'Infraestructura',
              '16':"Política de Seguridad Alimentaria",
              '17':"Inclusión Productiva",
              '21':"IRACA",
              '22':"FEST",
              '25':'Generación de Ingresos',
              '12':'Transferencias Monetarias Condicionadas',
              '20':'Transferencias Monetarias no Condicionadas',
              '23':'Colombia Mayor'}

dir_names = {'Inclusión Productiva':['13','16','17','21','22','25'],
        'Infraestructura':['14'],
        'Transferencias Monetarias':['12','20','23']}

def find_key(dictionary, value):
    for key, values in dictionary.items():
        if value in values:
            return key
    return None

# Función
def filter_rubros(data):
    data['Index_Rubro'] = data.apply(lambda x: x['Rubro'].split("-")[3], axis = 1)
    data = data[data['Index_Rubro'].str.contains('12|13|14|16|17|20|21|22|23|25', case = False, regex = True)].reset_index(drop = True)
    data['Descripción Rubro'] = data.apply(lambda x: rubro_names[x['Index_Rubro']], axis = 1)
    data = data.drop(data[data['Estado'] == 'Anulado'].index).reset_index(drop = True)
    data = data.drop(data[data['Estado'] == 'Anulada'].index).reset_index(drop = True)
    data['Dirección'] = data['Index_Rubro'].apply(lambda x: find_key(dir_names,x))
    data['Recurso'] = data['Recurso'].apply(lambda x: str(x).replace('\xa0', ' '))
    return data


cols_to_num ={'CDP':['Valor Inicial','Valor Operaciones','Valor Actual','Saldo por Comprometer'],
              'RP':['Valor Inicial', 'Valor Operaciones', 'Valor Actual', 'Saldo por Utilizar'],
              'Oblig':['Valor Inicial', 'Valor Operaciones','Valor Actual.1','Saldo por Utilizar'],
              'OP':['Valor Pesos', 'Valor Moneda', 'Valor Reintegrado Pesos', 'Valor Reintegrado Moneda'],
              }

def clean_bases(df1, dffip, tema):
    cols = cols_to_num[tema]
    cl1 = str_to_float(df1, cols)
    cl2 = str_to_float(dffip, cols)
    total = unificar_data(cl1, cl2)
    if tema == 'OP':
        total['Valor Neto Pesos'] = total.apply(lambda x: x['Valor Pesos']-x['Valor Reintegrado Pesos'], axis = 1)
    
    total = filter_rubros(total)
    
    return total


def clean_general(df):
    RG = df.dropna(subset = df.columns[0])
    RG['Index_Rubro'] = RG['RUBRO'].apply(lambda x: x.split("-")[-1])
    
    rec_names = {
    10:'RECURSOS CORRIENTES',
    11:'OTROS RECURSOS DEL TESORO',
    16:'FONDOS ESPECIALES'
    }

    RG = RG[(RG['Index_Rubro'].str.contains('12|13|14|16|17|20|21|22|23|25', case = False, regex = True)) & (RG['TIPO']=='C')].reset_index(drop = True)
    RG['Descripción Rubro'] = RG.apply(lambda x: rubro_names[x['Index_Rubro']], axis = 1)
    RG['Dirección'] = RG['Index_Rubro'].apply(lambda x: find_key(dir_names,x))
    RG['Recurso'] = RG['REC'].apply(lambda x: rec_names[int(x)])
    
    
    RG = RG.groupby(['Index_Rubro','Recurso']).agg({'Dirección':'first',
                                    'Descripción Rubro' : 'first',
                                    'APR. INICIAL' : 'sum',
                                    'APR. ADICIONADA' : 'sum',
                                    'APR. REDUCIDA' : 'sum',
                                    'APR. VIGENTE': 'sum',
                                    'APR BLOQUEADA': 'sum',
                                    'APR. DISPONIBLE' : 'sum',
                                    'CDP': 'sum',
                                   'COMPROMISO': 'sum',
                                   'OBLIGACION' : 'sum',
                                   'ORDEN PAGO' : 'sum',
                                   'PAGOS' : 'sum'}).reset_index(drop = False)
    
    return RG

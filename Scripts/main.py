import pandas as pd
from datetime import datetime
from Load_Data import get_data
from Modulo_1 import clean_bases, clean_general
from Modulo_2 import get_pre_second_base
from Modulo_3 import get_third_base
from Modulo_4 import get_fourth_base
from export import export_data


def get_date():
    while True:
        fecha_str = input("Ingrese una fecha (dd/mm/aaaa): ")

        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha inválida. Por favor ingrese una fecha en el formato dd/mm/aaaa.")
    
    return fecha

def run_code():
    ## Solicitamos la información
    bases_de_datos = get_data()
    
    ## Creamos el archivo donde se va a guardar todos los resultados
    resultados = dict()
    
    ## Solicitamos la fecha de actualización
    fecha = get_date()
    num_mes = fecha.month
    str_fecha = fecha.strftime("%Y/%m/%d")
    
    ## Listamos los archivos que fueron adquiridos
    archivos = list(bases_de_datos.keys())
    
    ## Enlistamos los archivos de FIP y NO FIP
    no_general_no_fip = [i for i in archivos if i!='Ejecución_Presupuestal_Agregada' and 'FIP' not in i]
    no_general_si_fip = [i for i in archivos if i!='Ejecución_Presupuestal_Agregada' and 'FIP' in i]
    
    ## Para cada pareja de tema + FIP hacemos la limpieza inicial
    ## Modulo 1
    for pair in [[i,j] for i,j in zip(no_general_no_fip,no_general_si_fip)]:
        try:
            resultados['G'+pair[0]] = clean_bases(bases_de_datos[pair[0]], bases_de_datos[pair[1]], pair[0])
        except:
            print("Problema con la base de datos: ",pair)
    
    ## Modulo 3
    try:
        resultados['Base_Compromisos'] = get_third_base(resultados['GRP'], resultados['GOblig'], resultados['GOP'])
        resultados['Base_Compromisos_Reservas'] = get_third_base(resultados['GRP_Reservas'], resultados['GOblig_Reservas'], resultados['GOP_Reservas'])
    except:
        pass
    ## Modulo 4
    try:
        resultados['BASE_RP_OP'] = get_fourth_base(resultados['GRP'], resultados['GOP'], num_mes)
    except:
        pass
    ## Si se cargo la Ejecución Presupuestal Agregada corremos el código para hacer el reporte general
    ## Y corremos aquellas funciones que realizan cambios sobre la base general
    ## Modulo 1
    ## Modulo 2
    if 'Ejecución_Presupuestal_Agregada' in archivos:
        try:
            resultados['RG'] = clean_general(bases_de_datos['Ejecución_Presupuestal_Agregada'])
        except: 
            pass
    
        try:
            resultados['Base_Rubros'] = get_pre_second_base(resultados['RG'], resultados['GCDP'], resultados['GRP'], resultados['GOblig'], 
                                                                      resultados['GOP'], num_mes)
        except:
            pass
        
    resultados['dates'] = pd.DataFrame({'Fecha':[fecha.strftime("%Y-%m-%d")]})
    
    return resultados


if __name__ == '__main__':
    resultados = run_code()
    export_data(resultados)

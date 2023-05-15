import pandas as pd
from datetime import datetime
from Load_Data import get_data
from Modulo_1 import clean_bases, clean_general, clean_general_DIP
from Modulo_2 import get_pre_second_base
from Modulo_3 import get_third_base
from Modulo_4 import get_fourth_base
from Modulo_5 import get_comparativa_2022
from export import export_data
from Create_Report import datos_excel, ctr_reservas



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
    
    ## Modulo 1:
    ### Limpieza de Bases Normales
    try:
        resultados['CDP'] = clean_bases(bases_de_datos['CDP'], bases_de_datos['CDP_FIP'],'CDP')
        resultados['RP'] = clean_bases(bases_de_datos['RP'], bases_de_datos['RP_FIP'], 'RP') 
        resultados['Oblig'] = clean_bases(bases_de_datos['Oblig'], bases_de_datos['Oblig_FIP'], 'Oblig') 
        resultados['OP'] = clean_bases(bases_de_datos['OP'], bases_de_datos['OP_FIP'], 'OP') 
        resultados['RP_Reserva'] = clean_bases(bases_de_datos['RP_Reservas'], bases_de_datos['RP_FIP_Reservas'], 'RP') 
        resultados['Oblig_Reserva'] = clean_bases(bases_de_datos['Oblig_Reservas'],bases_de_datos['Oblig_FIP_Reservas'], 'Oblig') 
        resultados['OP_Reserva'] = clean_bases(bases_de_datos['OP_Reservas'], bases_de_datos['OP_FIP_Reservas'], 'OP') 
        resultados['CDP_22'] = clean_bases(bases_de_datos['CDP_22'], bases_de_datos['CDP_FIP_22'], 'CDP') 
        resultados['RP_22'] = clean_bases(bases_de_datos['RP_22'], bases_de_datos['RP_FIP_22'], 'RP') 
        resultados['Oblig_22'] = clean_bases(bases_de_datos['Oblig_22'], bases_de_datos['Oblig_FIP_22'], 'Oblig')    
        resultados['OP_22'] = clean_bases(bases_de_datos['OP_22'], bases_de_datos['OP_FIP_22'], 'OP') 
    except:
        print('Problemas en la sección 1')
        raise

    ### Limpieza de Reportes Generales
    try:
        resultados['RG'] = clean_general(bases_de_datos['Ejecución_Presupuestal_Agregada'])
        resultados['RG22'] = clean_general(bases_de_datos['Ejecución_Presupuestal_Agregada_22'])
        
    except:
        print("Problemas con los reportes generales")
        raise
    
    ### Creamos los documentos de Excel
    try:
        resultados['RG_Excel'] = clean_general_DIP(bases_de_datos['Ejecución_Presupuestal_Agregada'])
        resultados['RG_Excel'] = datos_excel(resultados['RG_Excel'])
    except:
        print('Problemas con la creación de los archivos excel')
        raise
    
    ## Modulo 2
    try:
        resultados['Base_Rubros'] = get_pre_second_base(resultados['RG'], resultados['CDP'], resultados['RP'], resultados['Oblig'], 
                                                                      resultados['OP'], num_mes)
    
        resultados['Base_Rubros_22'] = get_pre_second_base(resultados['RG22'], resultados['CDP_22'], resultados['RP_22'], resultados['Oblig_22'], 
                                                                      resultados['OP_22'], 12)
    
    ## Creación Base Comparativa
        resultados['Base_Comparativa'] = get_comparativa_2022(resultados['Base_Rubros_22'], resultados['Base_Rubros'])
    
    except:
        print("Problemas en el módulo 2")
        raise
    ## Modulo 3
    try:
        resultados['Base_Compromisos'] = get_third_base(resultados['RP'], resultados['Oblig'], resultados['OP'])
        resultados['Base_Compromisos_Reservas'] = get_third_base(resultados['RP_Reserva'], resultados['Oblig_Reserva'], resultados['OP_Reserva'])
        resultados['Reservas_Excel'] = ctr_reservas(resultados['Base_Compromisos_Reservas'])
    except:
        print("Problemas en la sección 3")
        raise
    ## Modulo 4
    try:
        resultados['BASE_RP_OP'] = get_fourth_base(resultados['RP'], resultados['OP'], num_mes)
    except:
        print("Problemas en la sección 4")
        raise
    
    resultados['dates'] = pd.DataFrame({'Fecha':[fecha.strftime("%Y-%m-%d")]})
    
    return resultados


if __name__ == '__main__':
    resultados = run_code()
    export_data(resultados)

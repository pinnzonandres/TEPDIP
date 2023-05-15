# Se importan las librerías necesarias para el funcionamiento del código
import os
import pandas as pd

# Se define un diccionario que mapea cada archivo a sus correspondientes bases de datos
base_nuevos = {
    'CDP': {'file' : '1 CDP', 'header' : 0},
    'CDP_FIP' : {'file' : '5 CDP', 'header' : 0},
    'RP' : {'file' : '2 RP', 'header' : 0},
    'RP_FIP' : {'file' : '6 RP', 'header' : 0},
    'Oblig' : {'file' : '3 Oblig', 'header' : 0},
    'Oblig_FIP' : {'file' : '7 Oblig','header' : 0},
    'OP': {'file' : '4 OP', 'header' : 0},
    'OP_FIP': {'file' : '8 OP', 'header' : 0},
    'Ejecución_Presupuestal_Agregada': {'file' : 'EjecucionPresupuestalAgregada', 'header' : 3},
    'Oblig_Reservas': {'file' : '3.1 Oblig', 'header' : 0},
    'Oblig_FIP_Reservas': {'file' : '7.1 Oblig', 'header': 0},
    'OP_Reservas': {'file' : '4.1 OP', 'header' : 0},
    'OP_FIP_Reservas': {'file' : '8.1 OP', 'header' : 0},
}

base_reservas = {
    'RP_Reservas': {'file' : '2.1 RP', 'header': 0},
    'RP_FIP_Reservas': {'file' : '6.1 RP', 'header': 0},
}

base_2022 = {
    'CDP_22': {'file' : '1 CDP', 'header' : 0},
    'CDP_FIP_22' : {'file' : '5 CDP', 'header' : 0},
    'RP_22' : {'file' : '2 RP', 'header' : 0},
    'RP_FIP_22' : {'file' : '6 RP', 'header' : 0},
    'Oblig_22' : {'file' : '3 Oblig', 'header' : 0},
    'Oblig_FIP_22' : {'file' : '7 Oblig','header' : 0},
    'OP_22': {'file' : '4 OP', 'header' : 0},
    'OP_FIP_22': {'file' : '8 OP', 'header' : 0},
    'Ejecución_Presupuestal_Agregada_22': {'file' : 'EjecucionPresupuestalAgregada', 'header' : 3}
}

database = {
    'CDP': None,
    'CDP_FIP' : None ,
    'RP' : None ,
    'RP_FIP' : None ,
    'Oblig' : None ,
    'Oblig_FIP' : None ,
    'OP': None ,
    'OP_FIP': None ,
    'Ejecución_Presupuestal_Agregada': None,
    'Oblig_Reservas': None,
    'Oblig_FIP_Reservas': None,
    'OP_Reservas': None,
    'OP_FIP_Reservas': None,
    'RP_Reservas': None,
    'RP_FIP_Reservas': None,
    'CDP_22': None,
    'CDP_FIP_22' : None,
    'RP_22' : None,
    'RP_FIP_22' : None,
    'Oblig_22' : None,
    'Oblig_FIP_22' : None,
    'OP_22': None,
    'OP_FIP_22': None,
    'Ejecución_Presupuestal_Agregada_22': None
}

# Se define una función para cargar los datos
def get_data():
    script_dir = os.path.dirname(__file__)
    ruta_nuevos = os.path.join(script_dir, '..', 'Archivos Base', 'Reportes SIIF')
    ruta_carpeta_reciente = os.path.join(ruta_nuevos,sorted(os.listdir(ruta_nuevos))[-1])
    print("Se están cargando los archivos de la carpeta,", ruta_carpeta_reciente)
    archivos_excel_nuevos = [f for f in os.listdir(ruta_carpeta_reciente) if f.endswith(".xlsx")]

    ruta_rev = os.path.join(script_dir, '..', 'Archivos Base', 'Archivos Reservas')
    archivos_excel_rev = [f for f in os.listdir(ruta_rev) if f.endswith(".xlsx")]

    ruta_2022 = os.path.join(script_dir, '..', 'Archivos Base', 'Base 2022')
    archivos_excel_2022 = [f for f in os.listdir(ruta_2022) if f.endswith(".xlsx")]
    
    data_nuevos = {i:{'file': os.path.join(ruta_carpeta_reciente, [n for n in archivos_excel_nuevos if base_nuevos[i]['file'] in n][-1]), 'header':base_nuevos[i]['header'] } for i in base_nuevos.keys()}              
    data_rev = {i: {'file': os.path.join(ruta_rev, [n for n in archivos_excel_rev if base_reservas[i]['file'] in n][-1]),'header':base_reservas[i]['header']} for i in base_reservas.keys()}    
    data_2022 = {i: {'file': os.path.join(ruta_2022, [n for n in archivos_excel_2022 if base_2022[i]['file'] in n][-1]), 'header': base_2022[i]['header']} for i in base_2022.keys()}    
    
    for i in data_nuevos.keys():
        try:
            database[i] = pd.read_excel(data_nuevos[i]['file'], header = data_nuevos[i]['header'])
        except:
            print("No se pudo cargar la base,",i)
            raise
    for i in data_rev.keys():
        try:
            database[i] = pd.read_excel(data_rev[i]['file'], header = data_rev[i]['header'])
        except:
            print("No se pudo cargar la base,",i)
            raise
    for i in data_2022.keys():
        try:
            database[i] = pd.read_excel(data_2022[i]['file'], header = data_2022[i]['header'])
        except:
            print("No se pudo cargar la base,",i)
            raise
        
    return database
    
    
    
    



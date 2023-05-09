import pandas as pd
import easygui
import os

def set_path(nombre_folder):
    folderpath = easygui.diropenbox(title="Seleccione el lugar donde desea guardar la información")
    nueva_carpeta_path = os.path.join(folderpath, nombre_folder)
    os.mkdir(nueva_carpeta_path)
    
    # Crea las tres subcarpetas dentro de la nueva carpeta
    base_tablero_path = os.path.join(nueva_carpeta_path, "Base_Tablero")
    os.mkdir(base_tablero_path)
    
    archivos_modificados_path = os.path.join(nueva_carpeta_path, "Archivos_Modificados")
    os.mkdir(archivos_modificados_path)
    
    archivos_formato_excel_path = os.path.join(nueva_carpeta_path, "Archivos_Formato_Excel")
    os.mkdir(archivos_formato_excel_path)
    
    return base_tablero_path, archivos_modificados_path, archivos_formato_excel_path

def export_data(bases_de_datos):
    path1, path2, path3 = set_path(bases_de_datos['dates']['Fecha'].values[0])
    
    bases = ['GCDP', 'GRP', 'GOblig', 
             'GOP', 'GRP_Reservas', 
             'GOblig_Reservas', 'GOP_Reservas', 
             'Base_Compromisos',
             'Base_Compromisos_Reservas', 
             'BASE_RP_OP', 'RG', 'Base_Rubros']
    nombres = ['1_CDP', '2_RP', '3_Oblig', 
             '4_OP', '2.1_RP_Reservas', 
             '3.1_Oblig_Reservas', '4.1_OP_Reservas', 
             '7_Base_Compromisos',
             '7.1_Base_Compromisos_Reservas', 
             '8_BASE_RP_OP', '5_Reporte General', '6_Base_Rubros']
    
    for pair in zip(bases, nombres):
        try:
            path_f = os.path.join(path2,pair[1])
            bases_de_datos[pair[0]].to_excel(path_f+'.xlsx', index = False, sheet_name =pair[1])
        except:
            print('No se logró exportar la base: ', pair[1])
# Se importan las librerías necesarias para el funcionamiento del código
import inquirer
import pandas as pd
import easygui

# Se definen las preguntas que se mostrarán al usuario a través de la librería inquirer
# El usuario deberá seleccionar uno o varios archivos a cargar
questions = [
  inquirer.Checkbox('Archivos',
                    message="Seleccione los archivos que va a cargar",
                    choices=['CDP','RP','Oblig','OP','Reporte General','Reservas']
                    ),
]

# Se define un diccionario que mapea cada archivo a sus correspondientes bases de datos
archivos = {
    'CDP':[
        'CDP',
        'CDP_FIP'
        ],
    'RP':[
        'RP',
        'RP_FIP'
        ],
    'Oblig':[
        'Oblig',
        'Oblig_FIP'
        ],
    'OP':[
        'OP',
        'OP_FIP'
        ],
    'Reporte General':'Ejecución_Presupuestal_Agregada',
    'Reservas':[
        'RP_Reservas',
        'RP_FIP_Reservas',
        'Oblig_Reservas',
        'Oblig_FIP_Reservas',
        'OP_Reservas',
        'OP_FIP_Reservas'
        ]
    }

# Se define una función que utiliza easygui para abrir un cuadro de diálogo para seleccionar un archivo de la carpeta
def get_file_dir(dato):
    path = easygui.fileopenbox(title=f'Seleccione el archivo {dato}')
    return path

# Se define una función que utiliza inquirer para mostrar al usuario la pregunta y se guarda la respuesta en la variable "answers"
# Se utiliza la variable "archivos" para cargar los archivos correspondientes según la respuesta del usuario
# Dependiendo del archivo seleccionado, se utiliza la función get_file_dir para abrir un cuadro de diálogo y seleccionar el archivo
# Para el archivo 'Reporte General' se utiliza pd.read_excel con la opción "header = 3" para cargar los datos del archivo en un DataFrame
# Para los demás archivos, se utiliza un loop for para iterar sobre cada base de datos y cargarlos en un DataFrame utilizando pd.read_excel
# Se devuelve un diccionario "dbs" que contiene los DataFrames cargados correspondientes a cada archivo seleccionado por el usuario
def get_data():
    answers = inquirer.prompt(questions)['Archivos']
    dbs = {}
    for answer in answers:
        if answer == 'Reporte General':
            path = get_file_dir(dato = archivos[answer])
            dbs[archivos[answer]] = pd.read_excel(path, header = 3)
        else:
            for database in archivos[answer]:
                path = get_file_dir(dato= database)
                dbs[database] = pd.read_excel(path)
    
    return dbs


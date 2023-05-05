import pandas as pd
from datetime import datetime
from Load_Data import get_data
from Modulo_1 import clean_bases, clean_general
from Modulo_2 import get_pre_second_base
from Modulo_3 import get_third_base
from Modulo_4 import get_fourth_base


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
    bases_de_datos = get_data()
    resultados = dict()
    fecha = get_date()
    month = fecha.month
    str_fecha = fecha.strftime("%Y/%m/%d")
    
    archivos = list(bases_de_datos.keys())
    

    
run_code()


import pandas as pd

def get_comparativa_2022(d2022,d2023):
    d2022['Vigencia'] = 2022
    d2023['Vigencia'] = 2023
    
    result = pd.concat([d2022,d2023], ignore_index = True)
    
    return result

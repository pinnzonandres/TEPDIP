import pandas as pd

def get_third_base(RP, OB, OP):
    
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
    
    GOB= OB.groupby(by = ['Compromisos','Index_Rubro','Recurso']).agg({'Valor Actual.1': 'sum'}).reset_index(drop = False)
    
    GOB = GOB.rename(columns = {'Valor Actual.1':'Valor Obligaciones'})
    
    GOP = OP.groupby(by = ['Compromisos','Index_Rubro','Recurso']).agg({'Valor Neto Pesos': 'sum'}).reset_index(drop = False)
    
    GOP = GOP.rename(columns = {'Valor Neto Pesos': 'Valor Ordenes de Pago'})
    
    result = GRP.merge(GOB, how = 'left', on = ['Compromisos','Index_Rubro','Recurso'])
    result = result.merge(GOP, how = 'left', on = ['Compromisos', 'Index_Rubro','Recurso'])
    
    result['Tipo Contratista'] = result['Tipo Identificacion'].apply(lambda x: 'Persona natural' if x =='Cédula de Ciudadanía' else 'Persona jurídica')
    
    return result


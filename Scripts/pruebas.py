import easygui

path = easygui.fileopenbox(title='Carga el Archivo', filetypes=".xlsx", multiple=True)

print(path)
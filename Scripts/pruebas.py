import os

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'Archivos Base', 'Base 2022')

print(data_dir)
print([f for f in os.listdir(data_dir) if f.endswith(".xlsx")])
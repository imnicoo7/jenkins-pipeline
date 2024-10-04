# leer_csv.py
import pandas as pd

def leer_tareas():
    df = pd.read_csv('resultado.csv')
    for index, row in df.iterrows():
        if row['Tarea'] == 'Hijo 1' and row['Estado'] == 'Pendiente':
            print('Hijo 1')
        elif row['Tarea'] == 'Hijo 2' and row['Estado'] == 'Pendiente':
            print('Hijo 2')

if __name__ == "__main__":
    leer_tareas()

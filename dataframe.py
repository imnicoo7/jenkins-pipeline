import pandas as pd

def generar_dataframe():
    # data frame generado
    data = {'Tarea': ['Hijo 1', 'Hijo 2'],
            'Estado': ['Pendiente', 'Completado']}
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo CSV para que lo use Jenkins
    df.to_csv('resultado.csv', index=False)

if __name__ == "__main__":
    generar_dataframe()

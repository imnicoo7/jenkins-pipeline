import sys
import re
import os
import pandas as pd
from io import StringIO

class DataOps_utils():
    
    def __init__(self, directory_path):
        """
        Inicializa la clase con el directorio donde se buscará el archivo README.md.
        
        Args:
            directory_path (str): Ruta del directorio donde se encuentra el archivo README.md.
        """
        self.directory_path = directory_path

    
    def get_real_file_path(self,directory_path,file_to_search):
        """
        Busca un archivo en un directorio dado y devuelve su ruta completa.

        Esta función busca un archivo dentro del directorio especificado. Si se 
        encuentra el archivo (coincidencia no sensible a mayúsculas), devuelve 
        la ruta completa del archivo. Si no se encuentra el archivo, devuelve la 
        ruta completa esperada asumiendo que el archivo existe en el directorio 
        especificado.

        Parámetros:
        directory_path (str): La ruta del directorio donde se realiza la búsqueda.
        file_to_search (str): El nombre del archivo a buscar.

        Retorna:
        str: La ruta completa al archivo si se encuentra, de lo contrario, la 
        ruta completa esperada.
        """
        child_paths = os.listdir(directory_path)
        try:
            output = [os.path.join(directory_path,x) for x in child_paths if x.upper() == file_to_search.upper() ][0]
        except IndexError:
            output = os.path.join(directory_path,file_to_search)
        return output 
    
    
    def find_readme_path(self):
        """
        Busca el archivo README.md en el directorio especificado.

        Esta función busca el archivo README.md en el directorio especificado 
        por self.directory_path. Si el archivo no existe, devuelve un mensaje 
        de error y False. Si el archivo existe, devuelve la ruta completa al archivo.

        Returns:
            str: La ruta completa al archivo README.md si existe.
            list: Una lista que contiene un mensaje de error y False si el archivo no existe.
        """
        readme_path =  self.get_real_file_path(self.directory_path,"README.md")
        if not os.path.exists(readme_path):
            return [f"El archivo {readme_path} no existe.",False]
        else:
            return readme_path
    

    def find_items_readme(self):
        """
        Busca y analiza la tabla de recursos en el archivo README.md.

        Esta función busca el archivo README.md
        Si el archivo README.md no existe, devuelve un mensaje de error y False.
        Si el archivo existe, lee su contenido y busca una tabla de recursos.
        La tabla debe tener las columnas 'Orden' y 'Hora' y otras columnas
        separadas por pipes '|'. La función devuelve las filas de la tabla 
        donde la columna 'Activar' tiene el valor 'SI'.

        Returns:
            pd.DataFrame: Un DataFrame con las filas de la tabla donde 'Activar' 
                        es 'SI', si la tabla existe y es válida.
            list: Una lista que contiene un mensaje de error y False si el archivo 
                README.md no existe o si la tabla no se encuentra en el archivo.
        """
        readme_path = self.find_readme_path()
        if isinstance(readme_path, list):
            return readme_path
        else:
            with open(readme_path, 'r') as file:
                contenido = file.read()
        
            tabla_match = re.search(r"\| Orden.*\| Hora \|((\n\|[-\|\s:0-9A-Z_a-z.]+\|)+)", contenido)

            if tabla_match:
                tabla = tabla_match.group(0)
                df = pd.read_csv(StringIO(tabla), sep="|", skipinitialspace=True)
                df.columns = [col.strip() for col in df.columns]
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                df.dropna(how='all', inplace=True)
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                df['Dependencia Anterior'] = df['Dependencia Anterior'].str.upper()
                df['Activar'] = df['Activar'].str.upper()
                df['Tipo Objeto'] = df['Tipo Objeto'].str.upper()
                consulta_programada = df[(df['Activar'] == 'SI')]
                
                return consulta_programada
            else:
                return [f"No se encontro tabla de recursos en {readme_path}",False]
    
    
    def leer_dependencias(self):
        """
        Analiza el DataFrame generado a partir del archivo README.md y determina las acciones a tomar.

        Esta función utiliza el DataFrame generado por find_items_readme para identificar las dependencias 
        según la columna 'Tipo Objeto'. Si el 'Tipo Objeto' es "KNIME" o "CONSULTA PROGRAMADA", se añade 
        una acción correspondiente a la lista de acciones a ejecutar.
        
        - Si el 'Tipo Objeto' es "KNIME", añade la acción 'KNIME'.
        - Si el 'Tipo Objeto' es "CONSULTA PROGRAMADA", añade la acción 'ConsultaProgramada'.

        Retorna una lista con las acciones identificadas.

        Returns:
            list: Una lista con las acciones que deben ser ejecutadas, basada en el tipo de objeto 
            en el DataFrame. Por ejemplo, 'KNIME' o 'ConsultaProgramada'.
        """
        
        acciones = []
        df = self.find_items_readme()
        
        if isinstance(df, pd.DataFrame):

            for index, row in df.iterrows():
                if 'KNIME' in row['Tipo Objeto']:
                    acciones.append('knime')
                elif 'CONSULTA PROGRAMADA' in row['Tipo Objeto']:
                    acciones.append('consultaprogramada')
        else:
            print(df[0])

        return acciones

if __name__ == "__main__":
    # La ruta del directorio se pasa como argumento al script
    directory_path = sys.argv[1]
    # directory_path = './DataOps'
    
    # Crear una instancia de la clase
    dataops = DataOps_utils(directory_path)
    
    # Llama a la función que encuentra las dependencias
    dependencias = dataops.find_items_readme()
    print(dependencias.to_string(index=False))

# Leer_readme.py

def leer_dependencias():
    dependencias = []  # Lista para almacenar todas las coincidencias
    with open('readme.md', 'r') as file:
        for line in file:
            if 'knime' in line.lower():
                dependencias.append('KNIME')  # Agregar 'KNIME' a la lista
            elif 'consultaprogramada' in line.lower():
                dependencias.append('ConsultaProgramada')  # Agregar 'ConsultaProgramada' a la lista
            else:
                dependencias.append('NoReconocido')  # Agregar 'NoReconocido' si no coincide con nada conocido
    return dependencias

# Si el archivo se ejecuta como script principal
if __name__ == "__main__":
    dependencias = leer_dependencias()
    for dep in dependencias:
        print(dep)  # Imprimir cada dependencia encontrada

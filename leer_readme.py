def leer_dependencias():
    with open('README.md', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if 'knime' in line.lower():
            print('KNIME')
        elif 'bq' in line.lower():  # Detecta BigQuery
            print('BigQuery')
        else:
            print('No es un proceso conocido.')

if __name__ == "__main__":
    leer_dependencias()

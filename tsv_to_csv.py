import pandas as pd
import sys

tsv_filename = sys.argv[1]
csv_filename = sys.argv[2]

def convert_to_csv():
    """
    la funcion busca el archivo que le hayamos pasado como primer parametro desde la terminal(tsv_filename)
    ,el cual tiene una codificacion utf-16le y esta separado por tabulaciones, lo convierte y guarda en un archivo csv
    con codificacion utf-8 y usar separador pipe.
    imprime un mensaje detallando si la operacion fue exitosa o ocurrio un error(especificando el mismo)
    """
    try:
        data = pd.read_csv(tsv_filename,sep='\t',encoding='utf-16le') #'datos_data_engineer.tsv'
        data.to_csv(csv_filename,sep='|',encoding='utf-8') #'datos_data_engineer_file.csv'
        print("el archivo tsv fue convertido a csv")
    except Exception as e:
        print("ocurrio un error :", e)

convert_to_csv()

#ejemplo de ejecucion: python tsv_to_csv.py 'datos_data_engineer.tsv' 'datos_data_engineer_file.csv'
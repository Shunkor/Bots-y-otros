####################################################################################################################
# Un pequeño codigo para convertir un archivo .csv de un sistema de gestion de usuario, a una base de datos        #
# convirtiendo valores para que sea compatible a la hora de cargar en Mikrotik, despetando el plan de cada usuario #
#  En el codigo llamado "mikrotik asistente.py" esta la parte que lee esta base de datos y la inserta en mikrotik  #
####################################################################################################################

import csv
import sqlite3


def leer():
    # Abrimos la base de datos para obtener la tabla clientes
    # y la imprimimos para visualizar
    # esto te sirve si queres consultar como estan los datos
    # en visual code con la extension sqlite3 podes vizualizarla desde ahi
    
    con = sqlite3.connect("empresa.db")
    cur = con.cursor()
    instruccion = f"SELECT * FROM clientes"
    cur.execute(instruccion)
    datos = cur.fetchall()
    con.commit()
    con.close()
    for data in datos:
        print(data[0])


def guarda(nombre, apellido, direccion, plan, ip, bloqueo):
    # Abrimos la base de datos para insertar valores nuevos
    # Importante que esta funcion inserta nuevos, no hace comprobacion
    # nueva linea por cada llamada
    
    con = sqlite3.connect("empresa.db")
    cur = con.cursor()
    instruccion = f"INSERT INTO clientes VALUES ('{nombre}', '{apellido}', '{direccion}', '{plan}', '{ip}', '{bloqueo}')"
    cur.execute(instruccion)
    con.commit()
    con.close()


if __name__ == "__main__":
    # Importante saber que este codigo esta hecho para ejecutarse una vez, ya que crea el archivo nuevo
    # y hace el proceso indicado y listo, eso es todo, no es un codigo completo que revisa si existe la tabla, etc.
    
    # Creamos el archivo empersa.db con la tabla clientes
    con = sqlite3.connect("empresa.db")
    cur = con.cursor()
    
    # Abrimos el archivo csv a convertir
    # Este archivo contiene varios datos de clientes
    
    with open('archivo.csv', 'r') as archivo_csv:
        
        lector_csv = csv.reader(archivo_csv)
        for i, fila in enumerate(lector_csv):
            # ahora recorremos las filas, pasamos a mayusculas lo que nos interesa
            if i == 0: continue
            NOMBRE = fila[6].upper()
            APELLIDO = fila[7].upper()
            DIRECCION = fila[8].upper()
            PLAN = fila[14].upper()
            BLOQUEO = fila[16].upper()

            # Detectamos si esta vacio sin direccion y rellenamos
            if DIRECCION == "": DIRECCION = "S/D"
            # Convertimos el plan al formato aceptable por mikrotik
            
            if PLAN == "PLAN IP PRIVADA 10 MB": PLAN = "10M"
            if PLAN == "PLAN IP PUBLICA 10 MB": PLAN = "10M"
            if PLAN == "PLAN IP PRIVADA 10 MB 2": PLAN = "10M"
            if PLAN == "PLAN IP PRIVADA 15 MB BAJADA 5 MB SUBIDA": PLAN = "15M"
            if PLAN == "PLAN IP PUBLICA 15MB BAJADA 5 MB SUBIDA": PLAN = "15M"
            if PLAN == "PLAN IP PRIVADA 25/10MB": PLAN = "25M"
            if PLAN == "PLAN IP PRIVADA 25/25 MB GARANTIZADO": PLAN = "25M"
            if PLAN == "PLAN IP PRIVADA 50MB": PLAN = "50M"
            IP = fila[19]
            cantidad = i
            # ahora llamamos la funcion guarda, que insertara en la db cada cliente
            
            guarda(NOMBRE, APELLIDO, DIRECCION, PLAN, IP, BLOQUEO)


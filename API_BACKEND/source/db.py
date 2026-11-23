import mysql.connector
import os # propia de python(no se instala), para poder usar las variables de entorno ya puestas en el OS
from dotenv import load_dotenv # la libreria q solo sirve para llamar a load_dotenv()

load_dotenv()  # Carga las variables de entorno desde el archivo .env en el OS

def obtener_db_conexion_manual():  #coneccion manual a la base de datos
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    return connection



#retorna 3 posibles resultados: pero siempre es un [{}]
#1. Si es una instrucción de modificación de datos / alteracion de la estructura, retorna [{}].
#2. Si es una instrucción de consulta de datos, retorna un arreglo de diccionarios        [{datos1},{datos2}].
#3. Si ocurre un error, propaga la excepcion
def ejecutar_instruccion(query:str, valores:tuple=None, autocommit:bool=False)->list[dict]:
    resultados = list(dict())

    conexion = obtener_db_conexion_manual()
    cursor = conexion.cursor(dictionary=True, buffered=True) # dictionary=True para que devuelva dicts en vez de tuplas

    try:
        if valores is None: #mandar a ejecutar la instrucción con/sin valores
            cursor.execute(query) 
        else:
            cursor.execute(query, valores)

        if autocommit: 
            conexion.commit() #si la instruccion(query) realiza "cualquier" alteracion de datos o estructura, se hace commit para CONFIRMAR los cambios en la base de datos
        else:
            resultados = cursor.fetchall() #si la instruccion(query) es de consultar datos, se obtienen/traen los resultados

    except Exception as e:
        print(f"Error interno: {e}")
        raise # Para propagar la excepción y que se pueda manejar mas arriba

    finally:
        cursor.close()
        conexion.close()

    return resultados


def ejecutar_insercion(query:str, valores:tuple=None)->int:
    conexion = obtener_db_conexion_manual()
    cursor = conexion.cursor()

    try:
        cursor.execute(query, valores)
        conexion.commit()
        id_generado = cursor.lastrowid

    except Exception as e:
        conexion.rollback()
        print(f"Error interno: {e}")
        raise

    finally:
        cursor.close()
        conexion.close()

    return id_generado

def ejecutar_transaccion(operaciones, datos:dict):
    conexion = obtener_db_conexion_manual()
    cursor = conexion.cursor(dictionary=True, buffered=True)

    try:
        conexion.start_transaction()
        error, resultado = operaciones(cursor, datos)
        if error:
            conexion.rollback()
        else:
            conexion.commit()

    except Exception as e:
        conexion.rollback()
        print(f"Error interno: {e}")
        raise

    finally:
        cursor.close()
        conexion.close()

    return error, resultado

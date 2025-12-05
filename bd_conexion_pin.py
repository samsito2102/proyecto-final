from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
import mysql.connector
from mysql.connector import Error

dht_sensor_port = 7 
dht_sensor_type = 0  # 0 = blue sensor

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sensores"
        )
        if conexion.is_connected():
            print("Conectado a MariaDB")
        return conexion
    except Error as e:
        print("Error conectando a MariaDB:", e)
        return None

conexion = conectar_db()
cursor = conexion.cursor() if conexion else None
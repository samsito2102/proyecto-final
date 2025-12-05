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
            user="sensores",
            password="1234",
            database="sensors"
        )
        if conexion.is_connected():
            print("Conectado a MariaDB")
        return conexion
    except Error as e:
        print("Error conectando a MariaDB:", e)
        return None

conexion = conectar_db()
cursor = conexion.cursor() if conexion else None

setRGB(0, 255, 0)

while True:
    try:
        [temp, hum] = dht(dht_sensor_port, dht_sensor_type)
        print("temp =", temp, "C\thumidity =", hum, "%")

        # Validación valores
        if isnan(temp) or isnan(hum):
            raise TypeError("nan error")

        # Mostrar en LCD
        setText_norefresh("Temp:" + str(temp) + "C\nHum:" + str(hum) + "%")

        # ---- Guardar en la base de datos ----
        if conexion is None or not conexion.is_connected():
            print("Reintentando conexión...")
            conexion = conectar_db()
            cursor = conexion.cursor() if conexion else None

        if conexion and conexion.is_connected():
            sql = "INSERT INTO datos (temperatura, humedad) VALUES (%s, %s)"
            valores = (float(temp), float(hum))
            cursor.execute(sql, valores)
            conexion.commit()
            print(" Datos guardados en la base de datos")

    except (IOError, TypeError) as e:
        print("Error:", e)
        setText("")

    except KeyboardInterrupt:
        print("Programa detenido.")
        setText("")
        break

    except Error as e:
        print("Error en MariaDB:", e)
        conexion = None  

    sleep(0.05)
#final

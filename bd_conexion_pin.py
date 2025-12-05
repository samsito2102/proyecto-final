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
            sql = "INSERT INTO dht11 (temperatura, humedad) VALUES (%s, %s)"
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

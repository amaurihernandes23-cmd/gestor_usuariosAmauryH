import mysql.connector

def conectar():
    #conectar la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="empresa",
    )

    if conn.is_connected():
        print("Conexión a la base de datos")
        
    return conn
conectar()
    
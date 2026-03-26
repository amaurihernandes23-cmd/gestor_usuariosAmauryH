import mysql.connector

    # Clase empleado
class empleado:

    def __init__(self, documento, nombre, apellido, cargo, horas_extra, bonificacion):
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.horas_extra = horas_extra
        self.bonificacion = bonificacion
    
    def salario_base(self):
    
        if self.cargo.lower() == "gerente":
            return 5000000
        elif self.cargo.lower() == "administrador":
            return 3500000
        elif self.cargo.lower() == "contador":
            return 2800000
        else:
            return 1800000
    
    def calcularsalario(self):

        salbase = self.salario_base()
        totalextras = self.horas_extra * 3000

        salariobru = salbase + totalextras + self.bonificacion

        salud = salariobru * 0.04
        pension = salariobru * 0.04

        salarioneto = salariobru - salud - pension

        return salariobru, salud, pension, salarioneto

class departamento:

    def __init__(self, area):
        self.area = area
        # conectar a la base de datos
conn = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="empresa"
)

cursor = conn.cursor()

if conn.is_connected():
    print("Conectado a la base de datos")


while True:

    print("Bienvenido al registro de usuarios")
    print("1. Registrar usuarios")
    print("2. Listar usuarios")
    print("4. Actualizar bonificación")
    print("3. Buscar empleado")
    print("5. Eliminar empleado")
    print("6. Reporte de nómina")
    print("7. Registrar áreas")
    print("8. Actualizar áreas")
    print("9. Eliminar áreas")
    print("10.  Listar dependencias")
    print("11. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":

        documento = input("Ingresar # de documento: ")
        nombre = input("Ingresar el nombre del empleado: ")
        apellido = input("Ingresar el apellido del empleado: ")
        cargo = input("Ingresar el cargo del empleado: ")
        horas_extra = int(input("Ingresa # de horas extra al mes trabajadas: "))
        bonificacion = float(input("Ingresar el valor de la bonificación: "))

        empleado = empleado(documento, nombre, apellido, cargo, horas_extra, bonificacion)

        salariobru, salud, pension, salarioneto = empleado.calcularsalario()

        print("\nRESUMEN DE LA NOMINA")
        print("Salario bruto:", salariobru)
        print("Valor salud:", salud)
        print("Valor pension:", pension)
        print("Salario neto a pagar:", salarioneto)

        sql = """INSERT INTO empleado
        (documento,nombre,apellido,cargo,salariobru,horas_extra,bonificacion,salud,pension,salarioneto)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        datos = (documento, nombre, apellido, cargo, salariobru, horas_extra, bonificacion, salud, pension, salarioneto)

        cursor.execute(sql, (datos),)
        conn.commit()

        print("\nEmpleado guardado en la base de datos")
        
        if resultado:
            departamento = resultado[0]
            
            datos = (documento, nombre, apellido, cargo, horas_extra, bonificacion, salariobru, salud, pension, salarioneto, departamento)
            cursor.execute(sql, datos)
            conn.commit()
            print("Empleado guardado en la base de datos")
        else:
            print("El departamento no existe")


    if opcion == "2":
            
        #listar los empleados registrados en la bd

        cursor.execute("SELECT * FROM empleado")
        empleado = cursor.fetchall() #para una lista

        for em in empleado:
            print(empleado)


    elif opcion == "3":
    #busqueda del empleado por # de documento

        documento = input("Ingresar # de documento a buscar : ")
        sql = "SELECT * FROM empleado WHERE documento=%s"
        cursor.execute(sql,(documento,))

        resultado = cursor.fetchone() #para buscar un solo valor

        if resultado:
            print(resultado)

        else:
            print("El número de documento no existe")


    elif opcion == "4":

        #actializar el valor de la bonificacion
        documento = input("Ingresar # de documento del empleado : ")
        nuevovalor = float(input("Ingresar el valor de la nueva bonificacion : "))

        #crear la sentencia sql para actualizar
        sql = "UPDATE empleado SET bonificacion =%s WHERE documento=%s"

        cursor.execute(sql,(nuevovalor,documento))
        conn.commit()

        print("Valor bonificacion actualiado")

    elif opcion == "5":

        #eliminar empleado
        documento = input("Ingresar # de documento empleado a eliminar : ")
        sql = "DELETE FROM empleado WHERE documento=%s"
        cursor.execute(sql,(documento,))
        conn.commit()

        print ("Empleado eliminado")

    elif opcion == "6":
        #mostrar la cantidad de empleados y el valor total de los sueldos
        cursor.execute("SELECT COUNT(*), SUM(salarioneto) FROM empleado")
        reporte = cursor.fetchone()

        print("Total de empleado : ",reporte[0])
        print("Total pagado de nomina : ",reporte[1])
        
    elif opcion == "7":
        #registar un area
        area = input("ingresar el nombre del area: ")
        sql = "INSERT INTO departamento (area) VALUES (%s)"
        cursor.execute(sql,(area,))
        conn.commit()

    elif opcion == "8":
        #actualizar el nombre del area
        id_area = int(input("Ingresar el # del área para actualizar : "))
        nuevo_nombre = input("Ingresar el nuevo nombre del área : ")
        sql = "UPDATE departamento SET area=%s WHERE id_area=%s"
        cursor.execute(sql,(nuevo_nombre,id_area))
        conn.commit()

    elif opcion == "9":
        #eliminar un area
        id_area = int(input("Ingresar el # del área para eliminar : "))
        sql = "DELETE FROM area WHERE id_area=%s"
        cursor.execute(sql,(id_area,))
        conn.commit()
        
    elif opcion == "10":
        #listar las dependencias
        cursor.execute("SELECT * FROM area")
        area = cursor.fetchall()
        for area in area:
            print(area)
    
    elif opcion == "11":
        print("salir")
        break
    else:
        print("Opcion invalida")
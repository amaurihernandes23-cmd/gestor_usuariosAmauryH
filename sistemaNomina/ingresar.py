import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="empresa"
)

if conn.is_connected():
    print("Conexión a la base de datos exitosa")

cursor = conn.cursor()


# =========================
# CLASE EMPLEADO
# =========================
class Empleado:
    def __init__(self, documento, nombre, apellido, cargo, horas_extra, bonificacion, departamento=None):
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.horas_extra = horas_extra
        self.bonificacion = bonificacion
        self.departamento = departamento

    def salario_base(self):
        if self.cargo.lower() == "gerente":
            return 5000000
        elif self.cargo.lower() == "administrador":
            return 3500000
        elif self.cargo.lower() == "contador":
            return 2800000
        else:
            return 1800000

    def calcular_salario(self):
        salbase = self.salario_base()
        total_extras = self.horas_extra * 3000
        salariobru = salbase + total_extras + self.bonificacion

        salud = salariobru * 0.04
        pension = salariobru * 0.04
        salarioneto = salariobru - salud - pension

        return salariobru, salud, pension, salarioneto


# =========================
# CLASE DEPARTAMENTO
# =========================
class Departamento:
    def __init__(self, area):
        self.nombre = area


# =========================
# CLASE USUARIO
# =========================
class Usuario:
    def __init__(self, usuario, password, documento=None):
        self.usuario = usuario
        self.password = password
        self.documento = documento
        self.rol = "empleado"

    def registrar_usuario(self):
        # Verificar que el empleado exista
        sql_emp = "SELECT documento FROM empleado WHERE documento = %s"
        cursor.execute(sql_emp, (self.documento,))
        resultado = cursor.fetchone()

        if resultado:
            sql = """INSERT INTO usuario (usuario, password, rol, documento)
                     VALUES (%s, %s, %s, %s)"""
            datos = (self.usuario, self.password, self.rol, self.documento)
            cursor.execute(sql, datos)
            conn.commit()
            print("Usuario empleado registrado correctamente")
        else:
            print("El empleado no existe en la base de datos")

    def inicio_sesion(self):
        sql = """SELECT rol, documento FROM usuario
                 WHERE usuario = %s AND password = %s"""
        cursor.execute(sql, (self.usuario, self.password))
        resultado = cursor.fetchone()

        if resultado:
            print("\nInicio de sesión exitoso")
            return resultado
        else:
            print("Usuario o contraseña incorrectos")
            return None


# =========================
# MENÚ PRINCIPAL
# =========================
while True:
    print("\n========== SISTEMA DE NÓMINA ==========")
    print("1. Iniciar sesión")
    print("2. Registrar usuario empleado")
    print("3. Salir")

    opc = input("Ingrese una opción: ")

    # =========================
    # INICIAR SESIÓN
    # =========================
    if opc == "1":
        usuario = input("Ingrese usuario: ")
        password = input("Ingrese contraseña: ")

        login = Usuario(usuario, password)
        resultado = login.inicio_sesion()

        if resultado:
            rol = resultado[0]
            documento_usuario = resultado[1]

            print("Rol:", rol)

            # =========================
            # MENÚ ADMINISTRADOR
            # =========================
            if rol == "administrador":
                while True:
                    print("\n========== MENÚ ADMINISTRADOR ==========")
                    print("1. Registrar departamento")
                    print("2. Registrar empleado")
                    print("3. Listar departamentos")
                    print("4. Listar empleados")
                    print("5. Buscar empleado")
                    print("6. Actualizar bonificación")
                    print("7. Actualizar departamento")
                    print("8. Eliminar empleado")
                    print("9. Reporte de nómina")
                    print("10. Salir")

                    opcion = input("Seleccione una opción: ")

                    # Registrar departamento
                    if opcion == "1":
                        nombre = input("Ingrese el nombre del área: ")
                        dep = Departamento(nombre)

                        sql = "INSERT INTO departamento (area) VALUES (%s)"
                        datos = (dep.nombre,)
                        cursor.execute(sql, datos)
                        conn.commit()

                        print("Área registrada correctamente")

                    # Registrar empleado
                    elif opcion == "2":
                        documento = input("Documento: ")
                        nombre = input("Nombre: ")
                        apellido = input("Apellido: ")
                        cargo = input("Cargo: ")
                        horas_extra = int(input("Horas extra: "))
                        bonificacion = float(input("Bonificación: "))
                        departamento = input("Ingrese el nombre del departamento: ")

                        emp = Empleado(documento, nombre, apellido, cargo, horas_extra, bonificacion, departamento)
                        salariobru, salud, pension, salarioneto = emp.calcular_salario()

                        print("\n===== RESUMEN DE NÓMINA =====")
                        print("Salario bruto:", salariobru)
                        print("Salud:", salud)
                        print("Pensión:", pension)
                        print("Salario neto:", salarioneto)

                        # Buscar ID del departamento
                        sql_dep = "SELECT id_area FROM departamento WHERE area = %s"
                        cursor.execute(sql_dep, (departamento,))
                        resultado_dep = cursor.fetchone()

                        if resultado_dep:
                            id_departamento = resultado_dep[0]

                            sql = """INSERT INTO empleado
                                     (documento, nombre, apellido, cargo, salariobru, horas_extra,
                                      bonificacion, salud, pension, salarioneto, id_area)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                            datos = (
                                documento, nombre, apellido, cargo,
                                salariobru, horas_extra, bonificacion,
                                salud, pension, salarioneto, id_departamento
                            )

                            cursor.execute(sql, datos)
                            conn.commit()

                            print("Empleado guardado correctamente")
                        else:
                            print("El departamento no existe")

                    # Listar departamentos
                    elif opcion == "3":
                        cursor.execute("SELECT * FROM departamento")
                        areas = cursor.fetchall()

                        print("\n===== LISTA DE DEPARTAMENTOS =====")
                        for area in areas:
                            print(area)

                    # Listar empleados
                    elif opcion == "4":
                        cursor.execute("SELECT * FROM empleado")
                        empleados = cursor.fetchall()

                        print("\n===== LISTA DE EMPLEADOS =====")
                        for emp in empleados:
                            print(emp)

                    # Buscar empleado
                    elif opcion == "5":
                        documento = input("Ingrese el documento del empleado a buscar: ")
                        sql = "SELECT * FROM empleado WHERE documento = %s"
                        cursor.execute(sql, (documento,))
                        resultado_emp = cursor.fetchone()

                        if resultado_emp:
                            print("\nEmpleado encontrado:")
                            print(resultado_emp)
                        else:
                            print("El número de documento no existe")

                    # Actualizar bonificación
                    elif opcion == "6":
                        documento = input("Ingrese el documento del empleado: ")
                        nuevovalor = float(input("Ingrese la nueva bonificación: "))

                        sql = "UPDATE empleado SET bonificacion = %s WHERE documento = %s"
                        cursor.execute(sql, (nuevovalor, documento))
                        conn.commit()

                        print("Bonificación actualizada correctamente")

                    # Actualizar departamento
                    elif opcion == "7":
                        id_area = int(input("Ingrese el ID del área a actualizar: "))
                        nuevo_nombre = input("Ingrese el nuevo nombre del área: ")

                        sql = "UPDATE departamento SET area = %s WHERE id_area = %s"
                        cursor.execute(sql, (nuevo_nombre, id_area))
                        conn.commit()

                        print("Departamento actualizado correctamente")

                    # Eliminar empleado
                    elif opcion == "8":
                        documento = input("Ingrese el documento del empleado a eliminar: ")
                        sql = "DELETE FROM empleado WHERE documento = %s"
                        cursor.execute(sql, (documento,))
                        conn.commit()

                        print("Empleado eliminado correctamente")

                    # Reporte nómina
                    elif opcion == "9":
                        cursor.execute("SELECT COUNT(*), SUM(salarioneto) FROM empleado")
                        reporte = cursor.fetchone()

                        print("\n===== REPORTE DE NÓMINA =====")
                        print("Total de empleados:", reporte[0])
                        print("Total pagado de nómina:", reporte[1])

                    # Salir
                    elif opcion == "10":
                        print("Saliendo del menú administrador...")
                        break

                    else:
                        print("Opción inválida")

            # =========================
            # MENÚ EMPLEADO
            # =========================
            elif rol == "empleado":
                while True:
                    print("\n========== MENÚ EMPLEADO ==========")
                    print("1. Mostrar datos del empleado")
                    print("2. Actualizar datos")
                    print("3. Consultar nómina")
                    print("4. Salir")

                    opcion = input("Ingrese una opción: ")

                    # Mostrar datos
                    if opcion == "1":
                        sql = """SELECT documento, nombre, apellido, cargo, horas_extra, bonificacion
                                 FROM empleado WHERE documento = %s"""
                        cursor.execute(sql, (documento_usuario,))
                        resultado_emp = cursor.fetchone()

                        if resultado_emp:
                            print("\n===== DATOS DEL EMPLEADO =====")
                            print(f"Documento: {resultado_emp[0]}")
                            print(f"Nombre: {resultado_emp[1]}")
                            print(f"Apellido: {resultado_emp[2]}")
                            print(f"Cargo: {resultado_emp[3]}")
                            print(f"Horas extra: {resultado_emp[4]}")
                            print(f"Bonificación: {resultado_emp[5]}")
                        else:
                            print("Empleado no existe")

                    # Actualizar datos
                    elif opcion == "2":
                        print("\n¿Qué dato desea actualizar?")
                        print("1. Nombre")
                        print("2. Apellido")
                        print("3. Cargo")
                        print("4. Horas extra")
                        print("5. Bonificación")

                        eleccion = input("Seleccione una opción: ")

                        if eleccion == "1":
                            nuevo_valor = input("Ingrese el nuevo nombre: ")
                            campo = "nombre"
                        elif eleccion == "2":
                            nuevo_valor = input("Ingrese el nuevo apellido: ")
                            campo = "apellido"
                        elif eleccion == "3":
                            nuevo_valor = input("Ingrese el nuevo cargo: ")
                            campo = "cargo"
                        elif eleccion == "4":
                            nuevo_valor = int(input("Ingrese las nuevas horas extra: "))
                            campo = "horas_extra"
                        elif eleccion == "5":
                            nuevo_valor = float(input("Ingrese la nueva bonificación: "))
                            campo = "bonificacion"
                        else:
                            print("Opción inválida")
                            continue

                        sql = f"UPDATE empleado SET {campo} = %s WHERE documento = %s"
                        cursor.execute(sql, (nuevo_valor, documento_usuario))
                        conn.commit()

                        print(f"{campo.capitalize()} actualizado correctamente")

                    # Consultar nómina
                    elif opcion == "3":
                        sql = """SELECT salariobru, salud, pension, salarioneto
                                 FROM empleado WHERE documento = %s"""
                        cursor.execute(sql, (documento_usuario,))
                        resultado_nomina = cursor.fetchone()

                        if resultado_nomina:
                            print("\n===== RESUMEN DE NÓMINA =====")
                            print(f"Salario bruto: {resultado_nomina[0]}")
                            print(f"Salud: {resultado_nomina[1]}")
                            print(f"Pensión: {resultado_nomina[2]}")
                            print(f"Salario neto: {resultado_nomina[3]}")
                        else:
                            print("Empleado no existe")

                    # Salir
                    elif opcion == "4":
                        print("Saliendo del menú empleado...")
                        break

                    else:
                        print("Opción inválida")

    # =========================
    # REGISTRAR USUARIO EMPLEADO
    # =========================
    elif opc == "2":
        usuario = input("Ingrese usuario: ")
        password = input("Ingrese contraseña: ")
        documento = input("Ingrese documento del empleado: ")

        usu = Usuario(usuario, password, documento)
        usu.registrar_usuario()

    # =========================
    # SALIR
    # =========================
    elif opc == "3":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida")
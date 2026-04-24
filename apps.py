from subprocess import CREATE_NEW_PROCESS_GROUP

from flask import Flask, render_template, url_for, request, flash, redirect, session
from database import conectar

apps = Flask(__name__)
apps.secret_key = "4648754"

# login
@apps.route('/')
def login():
    return render_template("login.html")



@apps.route('/login', methods=['POST'])
def login_form():
    user_input = request.form["txtusuario"]
    password_input = request.form["txtcontrasena"]

    con = conectar()
    cursor = con.cursor()

    sql = "SELECT * FROM usuario WHERE usuario = %s AND password = %s"
    cursor.execute(sql, (user_input, password_input))
    user = cursor.fetchone()

    cursor.close()
    con.close()

    if user:
        session['id_usuario'] = user[0]
        session['usuario'] = user[1]
        session['rol'] = user[3]
        session['documento'] = user[4]

        return redirect(url_for("inicio"))
    else:
        flash("Usuario o contraseña incorrecta", "danger")
        return redirect(url_for('login'))


# inicio
@apps.route('/inicio')
def inicio():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    con = conectar()
    cursor = con.cursor()

    if session['rol'] == 'admin':

        # admin
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        cursor.execute("SELECT * FROM empleado")
        empleados = cursor.fetchall()
    else:
        # empleado
        cursor.execute("SELECT * FROM empleado WHERE documento = %s", (session['documento'],))
        empleados = cursor.fetchall()
        usuarios = []

    cursor.close()
    con.close()

    return render_template('index.html', user=usuarios, emple=empleados)


# salir
@apps.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))


# eliminar usuario
@apps.route('/eliminar/<int:id>')
def eliminarusu(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 'admin':
        flash("No tienes permiso", "danger")
        return redirect(url_for('inicio'))

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT rol FROM usuario WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()

    if usuario:
        if usuario[0] == "admin":
            flash("No se puede eliminar el administrador", "warning")
        else:
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id,))
            con.commit()
            flash("Usuario eliminado", "success")

    cursor.close()
    con.close()

    return redirect(url_for("inicio"))


#guardar usuario
@apps.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 'admin':
        flash("No tienes permiso", "danger")
        return redirect(url_for('inicio'))

    usuario = request.form["txtusuario"]
    password = request.form["txtcontrasena"]
    rol = request.form["txtrol"]
    documento = request.form["txtdocumento"]

    con = conectar()
    cursor = con.cursor()

    sql = "INSERT INTO usuario (usuario, password, rol, documento) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (usuario, password, rol, documento))

    con.commit()
    cursor.close()
    con.close()

    flash("Usuario registrado", "success")
    return redirect(url_for("inicio"))


# registrar empleado
@apps.route("/registrar_empleado", methods=["POST"])
def registrar_empleado():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 'admin':
        flash("No tienes permiso", "danger")
        return redirect(url_for('inicio'))

    documento = request.form["documento"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    cargo = request.form["cargo"]
    hora_extra = int(request.form["hora_extra"])
    bonificacion = float(request.form["bonificacion"])
    departamento = request.form["departamento"]

    # salario base
    def salario_base(cargo):
        if cargo == "gerente":
            return 5000000
        elif cargo == "administrador":
            return 3500000
        elif cargo == "contador":
            return 2800000
        else:
            return 1800000

    salariobase = salario_base(cargo)
    valorhora_extra = hora_extra * 3000
    salariobru = salariobase + valorhora_extra + bonificacion
    salud = salariobru * 0.04
    pension = salariobru * 0.04
    salarioneto = salariobru - salud - pension

    con = conectar()
    cursor = con.cursor()

    sql = """INSERT INTO empleado 
    (nombre, documento, apellido, cargo, salariobru, horas_extra, bonificacion, salud, pension, salarioneto, departamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    datos = (
        nombre, documento, apellido, cargo,
        salariobru, hora_extra, bonificacion,
        salud, pension, salarioneto, departamento
    )

    cursor.execute(sql, datos)
    con.commit()

    cursor.close()
    con.close()

    flash("Empleado registrado correctamente", "success")
    return redirect(url_for("inicio"))


# editar usuario
@apps.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 'admin':
        flash("No tienes permiso", "danger")
        return redirect(url_for('inicio'))

    con = conectar()
    cursor = con.cursor()

    if request.method == "POST":
        usuario = request.form["txtusuario"]
        password = request.form["txtcontrasena"]
        rol = request.form["txtrol"]
        documento = request.form["txtdocumento"]

        sql = """UPDATE usuario SET usuario=%s, password=%s, rol=%s, documento=%s WHERE id_usuario=%s"""

        cursor.execute(sql, (usuario, password, rol, documento, id))
        con.commit()
        
        cursor.close()
        con.close()

        flash("Usuario actualizado", "success")
        return redirect(url_for("inicio"))

    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("editar_usuario.html", usuario=usuario)


#eliminar empleado
@apps.route('/eliminar_empleado/<int:id>')
def eliminar_empleado(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 'admin':
        flash("No tienes permiso", "danger")
        return redirect(url_for('inicio'))

    con = conectar()
    cursor = con.cursor()

    cursor.execute("DELETE FROM empleado WHERE id = %s", (id,))
    con.commit()

    cursor.close()
    con.close()

    flash("Empleado eliminado", "success")
    return redirect(url_for("inicio"))


# editar empleado
@apps.route('/editar_empleado/<int:id>', methods=["GET", "POST"])
def editar_empleado(id):
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 'admin':
        flash("No tienes permiso", "danger")
        return redirect(url_for('inicio'))

    con = conectar()
    cursor = con.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        departamento = request.form["departamento"]
        documento = request.form["documento"]
        

        sql = """UPDATE empleado SET nombre=%s, apellido=%s, departamento=%s, documento=%s WHERE id=%s"""

        cursor.execute(sql, (nombre, apellido, departamento, documento, id))
        con.commit()

        cursor.close()
        con.close()

        flash("Empleado actualizado", "success")
        return redirect(url_for("inicio"))

    cursor.execute("SELECT * FROM empleado WHERE id = %s", (id,))
    empleado = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("editar_empleado.html", empleado=empleado)


# perfil empleado
@apps.route('/mi_perfil', methods=["GET", "POST"])
def mi_perfil():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    con = conectar()
    cursor = con.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        departamento = request.form["departamento"]
    
        sql = """UPDATE empleado SET nombre=%s, apellido=%s, departamento=%s WHERE documento=%s"""

        cursor.execute(sql, (nombre, apellido, departamento, session['documento']))
        con.commit()

        flash("Datos actualizados", "success")

    cursor.execute("SELECT * FROM empleado WHERE documento = %s", (session['documento'],))
    empleado = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("mi_perfil.html", empleado=empleado)


if __name__ == "__main__":
    apps.run(debug=True)
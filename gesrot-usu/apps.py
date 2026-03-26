from flask import Flask , render_template, url_for, request, flash, redirect
from database import conectar

apps = Flask (__name__)
apps.secret_key = "4648754"
@apps.route('/')
def login():
    return render_template("login.html")

@apps.route('/login',methods=["POST"])
def login_form():
    user = request.form["txtusuario"]
    password = request.form["txtcontrasena"]
    
    con = conectar()
    cursor = con.cursor()
    
    sql = "SELECT * FROM usuarios WHERE usuarios=% AND password=%" 
    cursor.execute(sql(user, password))
    user = cursor.fletchone 
    
    if user:
        rol = user[3] 
        if rol == rol:
            if rol == "administrador":
                return "Bienvenido administrador"
            else: 
                return "Bienvenido empleado"
        else:
            return "Rol incorrecto"
    else:
        flash ("Uusario o contraseña incorrecta" , "danger")
        return redirect(url_for('login.html'))
        
    

if __name__ == "__main__":
    apps.run(debug=True)
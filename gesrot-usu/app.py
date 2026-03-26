from flask import Flask,render_template,request
from database import conectar
#crear la app del proyecto 

app = Flask(__name__)

#crear la ruta principal 

@app.route('/')
def inicio():
    return render_template("index.html")
#crear la ruta para registrar los usuarios 

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    usuario = request.form['txtnombre']
    password = request.form['txtcontraseña']
    rol = request.form['txtrol']
    documento = request.form['documento']

    #llamar a la conexion
    con = conectar()
    cursor = con.cursor()

    #crear el sql 
       
    sql = """INSERT INTO usuario (usuario,password,rol,documento) VALUES (%s,%s,%s,%s)"""
    cursor.execute(sql,(usuario ,password ,rol ,documento))
    return "Usuario Guardado correctamente"
if __name__== '__main__':
    app.run(debug=True)


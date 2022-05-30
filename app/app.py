

from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import win32api
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuracion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'granjachame'
mysql = MySQL(app)

# configuraciones
app.secret_key = 'mysecretkey'


@app.route("/")
def index():
    return render_template("index.html")

   # return "hola mundoooo"
#   cur = mysql.connection.cursor()
#   cur.execute('SELECT * FROM usuarios')
#   datos= cur.fetchall()
  # return render_template("index.html", informacion= datos)

# @app.route("/envio", methods=['POST'])
# def enviar():
#   if request.method == 'POST':
#      fullname = request.form['nombre']
#      korreo = request.form['email']
#      estatus = request.form['status']
#      cur = mysql.connection.cursor()
#      cur.execute('INSERT INTO usuarios (nombre, correo, Estatus) VALUES (%s , %s, %s)',(fullname, korreo, estatus))
#      mysql.connection.commit()
#      flash("Se ha añadido un usuario")
#      return redirect(url_for("index"))

# @app.route("/actualizar/<id>", methods=['POST'])
# def actualizar(id):
#   if request.method == 'POST':
#      fullname = request.form['nombre']
#      korreo = request.form['email']
#      estatus = request.form['status']
#      cur = mysql.connection.cursor()
#      cur.execute("""
#         UPDATE usuarios
#         SET nombre = %s,
#             correo= %s,
#             Estatus= %s
#         WHERE id = %s
#      """, (fullname, korreo, estatus, id))
#      mysql.connection.commit()
#      flash("Se ha Actualizado la informacion del usuario")
#      return redirect(url_for("index"))

# @app.route("/editar/<id>")
# def modificar(id):
#   cur = mysql.connection.cursor()
#   cur.execute('SELECT * FROM usuarios WHERE id = %s', (id))
#   dato = cur.fetchall()
#   return render_template("editar.html", informacion = dato[0])

# @app.route("/borrar/<string:id>")
# def borrar(id):
#   cur = mysql.connection.cursor()
#   cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
#   mysql.connection.commit()
#   flash("El contacto se ha eliminado")
#   return redirect(url_for("index"))


@app.route("/post")
def post():
    s = Service('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe')
    s = Service('msedgedriver.exe')
    browser = webdriver.Edge(service=s)
    url_inicial = 'https://www.porcicultura.com/destacado/precios-del-cerdo-en-pie-en-mexico'
    browser.get(url_inicial)
    costoActual = list()
    fechaLeida=browser.find_element(by=By.XPATH, value='//*[@id="PrimeraFecha_PromedioNacionales"]')
    precioNacional = browser.find_element(by=By.XPATH, value='//*[@id="tbPromedioNacionales"]/tr/td[2]')
    costoActual.append(precioNacional.text)
    costoActual.append(fechaLeida.text)
    return render_template("post.html", informacion=costoActual)
    #return render_template("post.html")


@app.route("/raspador")
def raspador():
    return render_template("raspador.html")

@app.route("/prueba")
def prueba():
    return render_template("prueba.html")


@app.route("/envio")
def envio():

    # return render_template("raspador.html")
    s = Service('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe')
    s = Service('msedgedriver.exe')
    browser = webdriver.Edge(service=s)
    url_inicial = 'https://www.porcicultura.com/destacado/precios-del-cerdo-en-pie-en-mexico'
    browser.get(url_inicial)
    prueba = list()
    costoActual = list()
    fechaLeida= browser.find_element(by=By.XPATH, value='//*[@id="PrimeraFecha_PromedioNacionales"]')
    precioNacional = browser.find_element(by=By.XPATH, value='//*[@id="tbPromedioNacionales"]/tr/td[2]')
    precioEstados = browser.find_elements(by=By.CLASS_NAME, value='general')
    costoActual.append(precioNacional.text)
    for p in precioEstados:
        prueba.append(p.text)

    browser.quit()
    string = costoActual[0].strip('\""')
    print(string)

    with open('C:/Granja/archivos/precio.txt', "r") as archivo:

        for linea in archivo:
            cadena = linea

    if cadena == string:

        win32api.MessageBox(0, 'Vuelve a intentarlo otro día', 'Raspador Web', 0x00000001)
        palabras = "son iguales vuelve a intentarlo el dia de mañana"
    else:
        file = open('C:/Granja/archivos/precio.txt', "w")
        file.write(costoActual[0])
        file.close()
        win32api.MessageBox(0, 'Se ha actualizado el raspador', 'Raspador Web', 0x00000001)
        palabras = "Nuevo valor guardado"
    # pandas
        dfn = pd.DataFrame(prueba)
        path = 'C:\\Users\\52775\\Desktop\\Nueva carpeta\\NewInformacion.csv'
        dfn.to_csv(path, index=False, mode="a",header=not os.path.isfile(path))
    
    win32api.MessageBox( 0, 'El raspador se ejecuto correctamente', 'Raspador Web', 0x00000001)
#   return redirect(url_for("post"))
    return render_template("post.html", informacion= cadena )


@app.route("/modregresion")
def modregresion():
   datos = pd.read_csv('C:\\Granja\\archivos\\NewInformacion.csv', header=0, squeeze=True)
   with open("C:\\Users\\52775\\Desktop\\Nueva carpeta\\precio.txt", "r") as file:
# with open("C:/Users/52775/Desktop/Nueva carpeta/precio.txt","r") as archivo:

    for linea in file:
        cadena = linea

#print("valo de cadena es =" + cadena)
  # Vpredecir = float('36.85')
   Vpredecir = float(cadena)

   longitud = len(datos)
# for i in range(1, longitud+1):
   lst = [i for i in range(1, longitud+1)]

   x = np.array(lst).reshape((-1, 1))
   y = np.array(datos)
   model = LinearRegression()
   model.fit(x, y)
   x_new = np.array([Vpredecir]).reshape((-1, 1))
   y_new = model.predict(x_new)
   y_aproximado = float(y_new)
   bueno = format(y_aproximado, '.2f')  # give 2 digits after the point
  # print("Se deberia vender aproximadamente en ", bueno, "pesos por kilo", "hasta nuevo cambio")
   vprecio="Precio a vender", bueno
   plt.scatter(x, y)
   plt.plot(x, y, color='red', linewidth=3)
   plt.title('Regresion lineal simple')
   plt.text(9, 30, vprecio, fontsize=10, color='black')
   plt.text(1,41,"Mira como es el progreso del precio",fontsize=10, color='black')
   plt.xlabel('Numero de datos')
   plt.ylabel('precio por kilo')
   plt.show()

   return render_template("prueba.html", informacion = bueno)

if __name__ == "__main__":

    app.run(debug=True)

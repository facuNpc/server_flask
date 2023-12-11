
import traceback
from flask import Flask, request, jsonify, render_template, Response
# Base de datos
from flask_sqlalchemy import SQLAlchemy
# Crear el server Flask
app = Flask(__name__)

# Indicacion al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gastos.db"

# Asociacion de controlador de la base de datos con la aplicacion
db = SQLAlchemy()
db.init_app(app)

# ------------ Base de datos ----------------- #
class Gastos(db.Model):
    __tablename__ = "gastos"
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String)
    gasto = db.Column(db.Integer)


# ------------ Rutas o endpoints ----------------- #
# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/")
def index():
    try:
        result = "<h1>Bienvenido!!</h1>"
        result += "<h3>[GET] /iniciar --> endpoint utilizado para llenar la base de datos"
        result += "<h2>Alumno, Debe completar los siguientes endpoints en el backend:</h2>"
        result += "<h3>[GET] /gastos --> mostrar todo los gastos realizados en formato JSON"
        result += "<h3>[GET] /gastos/[categoria] --> mostrar todos los gastos de un categoría específica en formato JSON"
        return result
    except:
        # En caso de falla, retornar el mensaje de error
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/iniciar
@app.route("/iniciar")
def iniciar():
    try:
        # Borrar la base de datos antes de cargar los datos
        db.drop_all()

        # Volver a crear la base de datos
        db.create_all()

        # Cargar todos los datos
        gasto = Gastos(categoria="comida", gasto=30)
        db.session.add(gasto)
        gasto = Gastos(categoria="entretenimiento", gasto=50)
        db.session.add(gasto)
        gasto = Gastos(categoria="comida", gasto=50)
        db.session.add(gasto)
        gasto = Gastos(categoria="servicios", gasto=120)
        db.session.add(gasto)
        gasto = Gastos(categoria="servicios", gasto=100)
        db.session.add(gasto)
        gasto = Gastos(categoria="categoria", gasto=20)
        db.session.add(gasto)
        
        db.session.commit()

        return "datos generados"
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/gastos
@app.route("/gastos")
def gastos():
    try:
        print("Endpoint gastos")
        #leer datos
        query = db.session.query(Gastos)

        datos = []

        for row in query:
            json_result= {}
            json_result["categoria"] = row.categoria
            json_result["gasto"] = row.gasto
            datos.append(json_result)
        #devolver JSON
        return jsonify(datos)
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/gastos/<categoria>
@app.route("/gastos/<categoria>")
def gastos_categoria(categoria):
    try:
        print("Endpoint gastos_categoria")
        #leer base de datos y filtrar
        query = db.session.query(Gastos).filter(Gastos.categoria == categoria)

        datos = []

        for row in query:
            json_result= {}
            json_result["categoria"] = row.categoria
            json_result["gasto"] = row.gasto
            datos.append(json_result)
        #devolver JSON
        return jsonify(datos)

    except:
        return jsonify({'trace': traceback.format_exc()})


with app.app_context():
    #crear Base de Datos
    db.create_all()



if __name__ == '__main__':
    print('¡Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)

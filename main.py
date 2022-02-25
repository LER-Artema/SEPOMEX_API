import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# Importación de lista con el nombre de cada sheet del archivo excel y generador de api_key
from forms import estados, generate_api_key
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///SEPOMEX.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)



# tabla de llaves API
class API_KEY(db.Model):
    __tablename__ = 'API Keys'
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(250), nullable=False, unique=True)

# Tabla de Estados
class Estado(db.Model):
    __tablename__ = 'estados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    id_estado = db.Column(db.Integer, nullable=False)
    # Método para generar un diccionario compatible con Jsonfy
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Tabla de Colonias
class Colonia(db.Model):
    __tablename__ = 'colonias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    tipo_de_asentamiento = db.Column(db.String(250), nullable=False)
    id_de_asentamiento = db.Column(db.Integer, nullable=False)
    id_estado = db.Column(db.Integer, nullable=False)
    cp = db.Column(db.Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Tabla de Municipios
class Municipio(db.Model):
    __tablename__ = 'municipios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    id_estado = db.Column(db.Integer, nullable=False)
    id_mncp = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# db.create_all()
# ---------------------------------------- Creación de la base de Datos
# Loop que itera en la lista de nombres para generar un Dataframe por cada sheet de excel

# for estado in estados:
#     sheets = pd.read_excel('SEPOMEX_DATA.xls', sheet_name=estado)
#
# # Depuración de datos
#
#     sheets.drop(columns=['c_CP', 'd_ciudad', 'id_asenta_cpcons', 'd_CP', 'c_cve_ciudad'], axis=1, inplace=True)
#     sheets.dropna(inplace=True)

# Se itera en cada fila del DF y genera una lista con los valores de cada fila
#     for i in sheets.values:
#
#
#         estado = Estado(id_estado=i[5],
#                         nombre=i[4])
#         municipio = Municipio(id_mncp=i[8],
#                               nombre=i[3],
#                               id_estado=i[5])
#
#         colonia = Colonia(cp=i[0],
#                           nombre=i[1],
#                           tipo_de_asentamiento=i[2],
#                           id_de_asentamiento=i[7],
#                           id_estado=i[5])
#
#         db.session.add(estado)
#         db.session.add(municipio)
#         db.session.add(colonia)
#     db.session.commit()

# ------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para generar API Key y almacenarla en un archivo fuera del proyecto
@app.route("/generate_api_key")
def gen_api_key():
    password = generate_api_key()
    api_key = API_KEY(api_key=password)
    db.session.add(api_key)
    db.session.commit()
    return render_template('API_key.html', api_key=password)

@app.route("/search_cp")
# Ruta para buscar por codigo postal
def search_cp():
    api_key = request.args.get('api_key')
    api_key_ = db.session.query(API_KEY).filter_by(api_key=api_key).first()
    #  Si la API KEY se encuentra en la base de datos procede
    if api_key_:

        query_location = request.args.get("cp")
        colonias = db.session.query(Colonia).filter_by(cp=query_location)
        if colonias:
            # Jsonfy para devolver formato JSON
            return jsonify(colonias=[colonia.to_dict() for colonia in colonias])
        else:
            return jsonify(error={'El código postal ingresado no se encuentra en la base de datos'}), 404
    else:
        return jsonify(error='No cuentas con una API Key'), 403

@app.route('/search_municipio')
def search_municipio():
    api_key = request.args.get('api_key')
    api_key = db.session.query(API_KEY).filter_by(api_key=api_key).firts()
    if api_key:
        query_municipio = request.args.get("municipio")
        municipios = db.session.query(Municipio).filter_by(nombre=query_municipio)
        if municipios:
            return jsonify(municipios=[municipio.to_dict() for municipio in municipios])
        else:
            return jsonify(error={'El municipio ingresado no se encuentra en la base de datos'}), 404
    else:
        return jsonify(error='No cuentas con una API Key'), 403

@app.route('/search_colonia')
def search_colonia():
    api_key = request.args.get('api_key')
    api_key = db.session.query(API_KEY).filter_by(api_key=api_key).first()
    if api_key:
        query_colonia = request.args.get("colonia")
        colonias = db.session.query(Colonia).filter_by(nombre=query_colonia)
        if colonias:
            return jsonify(municipio=[colonia.to_dict() for colonia in colonias])
        else:
            return jsonify(error={'La colonia ingresada no se encuentra en la base de datos'}), 404
    else:
        return jsonify(error='No cuentas con una API Key'), 403

@app.route('/search_estado')
def search_estado():
    api_key = request.args.get('api_key')
    api_key = db.session.query(API_KEY).filter_by(api_key=api_key).firts()
    if api_key:
        query_estado = request.args.get("estado")
        estado = db.session.query(Estado).filter_by(nombre=query_estado)
        if estado:
            return jsonify(estados=estado.to_dict())
        else:
            return jsonify(error={'error': 'El estado ingresado no se encuentra en la base de datos'}), 404
    else:
        return jsonify(error='No cuentas con una API Key'), 403

@app.route("/add", methods=["POST"])
def add_location():
    api_key = request.args.get('api_key')
    api_key = db.session.query(API_KEY).filter_by(api_key=api_key).firts()
    if api_key:
        # Agrega nuevas tablas con los argumentos del request
        estado = Estado(id_estado=request.form.get('id_estado'),
                        nombre=request.form.get('nombre_estado'))
        municipio = Municipio(id_mncp=request.form.get('id_mncp'),
                              nombre=request.form.get('nombre_mncp'),
                              id_estado=request.form.get('id_estado'))

        colonia = Colonia(cp=request.form.get('código_postal'),
                          nombre=request.form.get('nombre_colonia'),
                          tipo_de_asentamiento=request.form.get('tipo_de_asentamiento'),
                          id_de_asentamiento=request.form.get('id_de_asentamiento'),
                          id_estado=request.form.get('id_estado'))

        db.session.add(estado)
        db.session.add(municipio)
        db.session.add(colonia)
        db.session.commit()
        return jsonify(response={"éxito": "Añadida nueva ubicacion"})
    else:
        return jsonify(error='No cuentas con una API Key'), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

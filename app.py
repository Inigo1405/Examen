from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
# from flask_cors import CORS


# Link github: https://github.com/Inigo1405/Examen
# Link rendeer: https://examen-2ejx.onrender.com/

load_dotenv()

app = Flask(__name__)
# CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
BASE_URL = '/api/v1'


class Videojuegos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(75), nullable=False)
    desarrollador = db.Column(db.String(120), nullable=False)
    anio_lanzamiento = db.Column(db.Integer, nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    clasificacion = db.Column(db.String(50), nullable=False)

    def __init__(self, titulo, desarrollador, anio_lanzamiento, plataforma, clasificacion):    
        self.titulo = titulo
        self.desarrollador = desarrollador
        self.anio_lanzamiento = anio_lanzamiento
        self.plataforma = plataforma
        self.clasificacion = clasificacion

    def to_json(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "desarrollador": self.desarrollador,
            "anio_lanzamiento": self.anio_lanzamiento,
            "plataforma": self.plataforma,
            "clasificacion": self.clasificacion,
        }

    def __repr__(self):
        return f'<Videojuego: {self.name}>'
    


@app.route(BASE_URL + '/new', methods=['POST'])
def create():
    if not request.json:
        abort(400)
        
    game = Videojuegos(titulo=request.json['titulo'], desarrollador=request.json['desarrollador'], anio_lanzamiento=request.json['anio_lanzamiento'], plataforma=request.json['plataforma'], clasificacion=request.json['clasificacion'])
    db.session.add(game)
    db.session.commit()
    return jsonify(game.to_json()), 201


# --- Read ---
@app.route(BASE_URL + '/read', methods=['GET'])
def read():
    games = Videojuegos.query.all()
    return jsonify([game.to_json() for game in games])


@app.route(BASE_URL + '/read/category/<category>', methods=['GET'])
def read_by_clasification(category:str):
    games = Videojuegos.query.filter(Videojuegos.clasificacion==category)
    return jsonify([game.to_json() for game in games])


@app.route(BASE_URL + '/read/year/<year>', methods=['GET'])
def read_by_year(year:int):
    games = Videojuegos.query.filter(Videojuegos.anio_lanzamiento==year)
    return jsonify([game.to_json() for game in games])


@app.route(BASE_URL + '/read/company/<company>', methods=['GET'])
def read_by_company(company:str):
    games = Videojuegos.query.filter(Videojuegos.desarrollador==company)
    return jsonify([game.to_json() for game in games])


@app.route(BASE_URL + '/read/plataform/<plataform>', methods=['GET'])
def read_by_plataform(plataform:str):
    games = Videojuegos.query.filter(Videojuegos.desarrollador==plataform)
    return jsonify([game.to_json() for game in games])
    



# --- Update ---
@app.route(BASE_URL + '/update/<id>', methods=['PUT'])
def update(id:int):
    game = Videojuegos.query.get(id)

    if not game:
        abort(304)

    return jsonify(game.to_json()), 202


@app.route(BASE_URL + '/delete', methods=['DELETE'])
def delete(id):
    game = Videojuegos.query.get_or_404(id)

    db.session.delete(game)
    db.session.commit()
    return jsonify(game.to_json()), 202


# --- MAIN -------------------------------------------------------------------- 
@app.route('/')
def index():
    return "Welcome to my ORM app Web: Videogames!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Tables created...")
    app.run(debug=False)
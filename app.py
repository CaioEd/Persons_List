from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# CONFIGURAÇÃO BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TABELA PERSONS
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(3))  
    type = db.Column(db.String(10))
    action = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50)) 

# CRIAÇÃO BANCO
@app.before_request
def create_tables():
    db.create_all()


json_url = "http://ec2-3-87-113-128.compute-1.amazonaws.com/records"

# ROTA HOME
@app.route('/')
def home():
    return('Hello, World!')


# ROTA GET - RETORNA TODOS OS USUÁRIOS
@app.route('/persons', methods=['GET'])
def get_persons():
    persons = Person.query.all()
    return jsonify([{
        "id": person.id,
        "age": person.age,
        "type": person.type,
        "action": person.action,
        "date": person.date
    } for person in persons])


# ROTA GET COM FILTRO POR ACTION
@app.route('/persons/<action>', methods=['GET'])
def get_persons_action(action):
    filtered_persons = Person.query.filter_by(action=action).all()

    if filtered_persons:
        return jsonify([{
            "id": person.id,
            "age": person.age,
            "type": person.type,
            "action": person.action,
            "date": person.date
        } for person in filtered_persons])
    else:
        return jsonify({"message": "Nenhum usuário encontrado!"}), 404


# ROTA POST - ADICIONA OS DADOS 
@app.route('/persons', methods=['POST'])
def add_persons():
    try:
        # REQUISIÇÃO
        response = requests.get(json_url)
        response.raise_for_status()
        new_persons = response.json()

        # ITERAÇÃO SOBRE A LISTA
        for person_data in new_persons:
            person = Person(
                age=person_data.get('age'),
                type=person_data.get('type'),
                action=person_data.get('action'),
                date=person_data.get('date')
            )

            db.session.add(person)

        db.session.commit()
        return jsonify({"message": "Dados inseridos!"}), 201
        
    except  requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
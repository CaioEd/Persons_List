from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# VARIÁVEL QUE GUARDA OS DADOS
data = [
    {"id": 1, "name": "Caio", "action": "comer"},
    {"id": 2, "name": "João", "action": "correr"},
    {"id": 3, "name": "Maria", "action": "dormir"}
]

json_url = "http://ec2-34-230-24-198.compute-1.amazonaws.com/records"

# ROTA HOME
@app.route('/')
def home():
    return('Hello, World!')


# ROTA GET - RETORNA TODOS OS USUÁRIO
@app.route('/persons', methods=['GET'])
def get_persons():
    return jsonify(data)


@app.route('/persons/<action>', methods=['GET'])
def get_persons_action(action):
    filtered_persons = [person for person in data if person['action'] == action]

    if filtered_persons:
        return jsonify(filtered_persons)
    else:
        return jsonify({"message": "Nenhum usuário encontrado com essa ação!"}), 404


@app.route('/persons', methods=['POST'])
def add_persons():

    response = requests.get(json_url)
    response.raise_for_status()

    new_persons = response.json()
    data.extend(new_persons)


if __name__ == '__main__':
    app.run(debug=True)

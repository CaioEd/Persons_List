from flask import Flask, jsonify
import json

app = Flask(__name__)

# CARREGAR JSON
def data_json():
    with open('data.json') as arquivo_json:
        data = json.load(arquivo_json)
    return data


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/persons', methods=['GET'])
def persons():
    data = data_json()
    return jsonify(data)


@app.route('/persons/<action>', methods=['GET'])
def person_action(action):
    data = data_json()

    # FILTRA USUÁRIOS QUE POSSUEM A AÇÃO
    filtrados = [person for person in data if person.get('action') == action]

    if filtrados:
        return jsonify(filtrados)
    else:
        return jsonify({"message": "Nenhum usuário encontrado!"})


if __name__ == '__main__':
    app.run(debug=True) 
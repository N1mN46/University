import json
import os
from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'data.json')
users_file = os.path.join(basedir, 'users.json')

def load_data(filename):
    if not os.path.exists(filename):
        return [] if filename == data_file else {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return [] if filename == data_file else {}
    
def save_data(filename, data_content):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_content, f, indent=4, ensure_ascii=False)


@auth.verify_password
def verify_password(username, password):
    users_load = load_data(users_file)
    if username in users_load and users_load[username] == password:
        return username
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/items', methods=['GET'])
@auth.login_required
def get_items():
    items = load_data(data_file)
    return jsonify(items)

@app.route('/items', methods=['POST'])
@auth.login_required
def create_item():
    if not request.json or not 'name' in request.json:
        abort(400, description="Missing 'name' in request body")
    
    items = load_data(data_file)

    new_id = 1
    if items:
        new_id = max(item['id'] for item in items) + 1

    new_item = {
        'id': new_id,
        'name': request.json['name'],
        'price': request.json.get('price', 0.0)
    }

    items.append(new_item)
    save_data(data_file, items)

    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
@auth.login_required
def get_item(item_id):
    items = load_data(data_file)
    item = next((item for item in items if item['id'] == item_id), None)

    if item is None:
        abort(404, description="Item not found")
    
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(item_id):
    if not request.json:
        abort(400, description="Request must be JSON")

    items = load_data(data_file)
    item = next((item for item in items if item['id'] == item_id), None)
    
    if item is None:
        abort(404, description="Item not found")

    item['name'] = request.json.get('name', item['name'])
    item['price'] = request.json.get('price', item['price'])

    save_data(data_file, items)
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(item_id):
    items = load_data(data_file)
    item = next((item for item in items if item['id'] == item_id), None)

    if item is None:
        abort(404, description="Item not found")
    
    items.remove(item)
    save_data(data_file, items)

    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'message': error.description}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'message': error.description}), 400)

if __name__ == '__main__':
    app.run(port=8000)
import datetime
from bson import ObjectId
import serializer
from flask import Flask, jsonify, make_response, request, abort, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

# Инициализируем БД
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/Dream")
db = mongodb_client.db


@app.route('/')
def index():
    data = db.Dream.find().sort("date", -1)
    data = serializer.serializer_find_all(data)
    return render_template('dream.html', data=data)


@app.route('/api/v1.0/dreams', methods=['GET'])
def get_dreams():
    return jsonify(serializer.serializer_find(db.Dream.find()))


@app.route('/api/v1.0/dream/<string:dream_id>', methods=['GET'])
def get_id_dream(dream_id):
    try:
        objInstance = ObjectId(dream_id)
        data = serializer.serializer_find_one(db.Dream.find_one({'_id': objInstance}))
    except:
        return jsonify({'Error': 'Invalid Id'})
    return jsonify(data)


@app.route('/api/v1.0/dreams_author/<string:author>', methods=['GET'])
def get_author_dream(author):
    try:
        data = serializer.serializer_find(db.Dream.find({'author': author}))
    except:
        return jsonify({'Error': 'Invalid author'})
    return jsonify(data)


@app.route('/api/v1.0/dream', methods=['POST'])
def create_dream():
    if not request.json or not 'title' in request.json:
        abort(400)
    dream = {
        'author': request.json['author'],
        'title': request.json['title'],
        'done': False,
        'date': datetime.datetime.now()
    }
    res = db.Dream.insert_one(dream)

    return jsonify({'dream': str(res.inserted_id),
                    'status': 'added'}), 201


@app.route('/api/v1.0/dream/<string:dream_id>', methods=['PUT'])
def update_dream(dream_id):
    if not request.json or not 'done' in request.json:
        abort(400)
    status = request.json['done']
    try:
        objInstance = ObjectId(dream_id)
        db.Dream.update_one({'_id': objInstance}, {'$set': {'done': status}})
        return jsonify({'dream': dream_id,
                        'status': 'updated'})
    except:
        return jsonify({'Error': 'Invalid Id'})


@app.route('/api/v1.0/dream/<string:dream_id>', methods=['DELETE'])
def delete_task(dream_id):
    try:
        objInstance = ObjectId(dream_id)
        db.Dream.delete_one({'_id': objInstance})
        return jsonify({'dream': dream_id,
                        'status': 'deleted'})
    except:
        return jsonify({'Error': 'Invalid Id'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_reques(error):
    return make_response(jsonify({'Error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(debug=False,
            host='0.0.0.0')

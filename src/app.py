"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def all_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members),200

@app.route('/members/<id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member),200

@app.route('/members/<id>', methods=['DELETE'])
def get_member(id):
    member = jackson_family.delete_member(id)
    return jsonify(member),200

@app.route('/member', methods=['POST'])
def create_one_member ():
    id = request.json.get('id')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    age = request.jason.get('age')
    lucky_number = request.get('lucky_number')

    if not id:
        id = jackson_family._generateId()
    if not first_name:
        return jsonify({"msg": "We need yor name"}), 400
    if not age:
        return jsonify({"msg": "We need yor age"}), 400
    if not lucky_number:
        return jsonify({"msg": "We need yor lucky_number"}), 400

    member = {}
    member['id'] = id
    member['first_name'] = first_name
    member['last_name'] = last_name
    member['age'] = age
    member['lucky_number'] = lucky_number

    jackson_family.add_member(member)
    return jsonify({"msg": "Member was create succefull"}), 200

    @app.route('/member', methods=['PUT'])
    def edit_member ():
        id = request.json.get('id')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        age = request.jason.get('age')
        lucky_number = request.get('lucky_number')



        if not id:
            id = jackson_family._generateId()
        if not first_name:
            return jsonify({"msg": "We need yor name"}), 400
        if not age:
            return jsonify({"msg": "We need yor age"}), 400
        if not lucky_number:
            return jsonify({"msg": "We need yor lucky_number"}), 400

        member = jackson_family.get_member(id)
        if not member:
            return jsonify({"msg": " Not found"}), 404
        if member:
            member['id'] = id
            member['first_name'] = first_name
            member['last_name'] = last_name
            member['age'] = age
            member['lucky_number'] = lucky_number

            jackson_family.update_member(id,member)
            return jsonify({"msg": "Member was updated"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

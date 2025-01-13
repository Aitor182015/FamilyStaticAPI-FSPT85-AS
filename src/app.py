import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

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

# Endpoint para obtener todos los mimbros de la familia. Modifico el enlace de /members a /member por comodidad a la hroa de hacer pruebas con postman
@app.route('/member', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    if not members:
        return jsonify({"message": "There are no members available"}), 404
    return jsonify(members), 200

# Endpoint para obtener a un unico miembro por su ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"message": "Member not found"}), 400
    return jsonify(member), 200

# Endpoint para añaadir un nuevo miembro
@app.route('/member', methods=['POST'])
def add_member():
    body = request.json
    if not body:
        return jsonify({"message": "Invalid input"}), 400

    new_member = {
        "first_name": body.get("first_name"),
        "age": body.get("age"),
        "lucky_numbers": body.get("lucky_numbers", []),
    }

    member = jackson_family.add_member(new_member)
    return jsonify(member), 200

# Endpoint para borrar un miembro por su ID
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if member is None:
        return jsonify({"message": "Member not found"}), 404
    return jsonify({"message": "Member deleted", "deleted_member": member}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

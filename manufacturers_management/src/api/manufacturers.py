from flask import request, jsonify, Blueprint, Response

from ..queries.get_manufacturers import GetManufacturer
from ..commands.create_manufacturers import CreateManufacturers
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..errors.errors import *

manufacturers = Blueprint('manufacturers', __name__)

@manufacturers.route('/manufacturers', methods=['POST'])
@jwt_required()
def create_manufacturers():
    data = request.get_json()
    try:
        result = CreateManufacturers(data).execute()
        return jsonify(result), 201
    except InvalidData as e:
        return jsonify({"error": e.description}), 400
    except InvalidName as e:
        return jsonify({"error": e.description}), 400
    except InvalidCountry as e:
        return jsonify({"error": e.description}), 400
    except InvalidContact as e:
        return jsonify({"error": e.description}), 400
    except InvalidTelephone as e:
        return jsonify({"error": e.description}), 400
    except InvalidEmail as e:
        return jsonify({"error": e.description}), 400

@manufacturers.route('/manufacturers/<string:manufacturer_name>', methods=['GET'])
@jwt_required()
def get_manufacturer(manufacturer_name):
    result = GetManufacturer(manufacturer_name).execute()
    return result

@manufacturers.route('/manufacturers/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200
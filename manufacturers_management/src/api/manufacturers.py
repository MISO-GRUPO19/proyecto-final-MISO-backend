from flask import request, jsonify, Blueprint, Response

from ..queries.get_manufacturers import GetManufacturer, GetManufacturerById, GetAllManufacturers
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

@manufacturers.route('/manufacturers/<uuid:manufacturer_id>', methods=['GET'])
@jwt_required()
def get_manufacturer_by_id(manufacturer_id):
    result = GetManufacturerById(manufacturer_id).execute()
    return result

@manufacturers.route('/manufacturers', methods=['GET'])
@jwt_required()
def get_manufacturers():
    manufacturer_name = request.args.get('name')
    
    if manufacturer_name:
        result = GetManufacturer(manufacturer_name).execute()
    else:
        result = GetAllManufacturers().execute()
    
    return result


@manufacturers.route('/manufacturers/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200
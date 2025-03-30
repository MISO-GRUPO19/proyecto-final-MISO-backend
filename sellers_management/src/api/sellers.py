from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..commands.create_sellers import CreateSellers
from ..errors.errors import *
sellers = Blueprint('sellers', __name__)

@sellers.route('/sellers', methods=['POST'])
@jwt_required()
def create_seller():
    data = request.get_json()
    try:
        result = CreateSellers(data).execute()
        return jsonify(result), 201
    except InvalidData as e:
        return jsonify({"error": e.description}), 400
    except InvalidIdentification as e:
        return jsonify({"error": e.description}), 400
    except InvalidName as e:
        return jsonify({"error": e.description}), 400
    except InvalidCountry as e:
        return jsonify({"error": e.description}), 400
    except InvalidAddress as e:
        return jsonify({"error": e.description}), 400
    except InvalidTelephone as e:
        return jsonify({"error": e.description}), 400
    except InvalidEmail as e:
        return jsonify({"error": e.description}), 400
@sellers.route('/sellers/ping', methods=['GET'])
def ping():
    return jsonify({"message": 'pong'}), 200
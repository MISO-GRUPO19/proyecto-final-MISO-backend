from flask import jsonify
from ..models.manufacturers import Manufacturers
from ..models.database import db_session
from ..errors.errors import NotExistingManufacturer

class GetManufacturer:
    def __init__(self, manufacturer_name: str):
        self.manufacturer_name = manufacturer_name

    def execute(self):
        with db_session() as session:
            manufacturer = session.query(Manufacturers).filter(Manufacturers.name == self.manufacturer_name).first()
            if not manufacturer:
                raise NotExistingManufacturer
            return jsonify({
                "name": manufacturer.name,
                "country": manufacturer.country,
                "contact": manufacturer.contact,
                "telephone": manufacturer.telephone,
                "email": manufacturer.email
            }), 200
            
class GetManufacturerById:
    def __init__(self, manufacturer_id: int):
        self.manufacturer_id = manufacturer_id
    
    def execute(self):
        with db_session() as session:
            manufacturer = session.query(Manufacturers).filter(Manufacturers.id == self.manufacturer_id).first()
            if not manufacturer:
                raise NotExistingManufacturer
            return jsonify({
                "name": manufacturer.name,
                "country": manufacturer.country,
                "contact": manufacturer.contact,
                "telephone": manufacturer.telephone,
                "email": manufacturer.email
            }), 200
            
class GetAllManufacturers:
    def __init__(self):
        pass
    def execute(self):
        with db_session() as session:
            manufacturers = session.query(Manufacturers).all()
            result = []
            for manufacturer in manufacturers:
                result.append({
                    "id": manufacturer.id,
                    "name": manufacturer.name,
                    "country": manufacturer.country,
                    "contact": manufacturer.contact,
                    "telephone": manufacturer.telephone,
                    "email": manufacturer.email
                })
            return jsonify(result), 200
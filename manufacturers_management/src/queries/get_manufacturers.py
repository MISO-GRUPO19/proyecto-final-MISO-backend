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
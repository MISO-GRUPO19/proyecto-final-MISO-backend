from .base_command import BaseCommand
from ..errors.errors import *
from ..models.manufacturers import Manufacturers
from ..models.database import db_session
from flask import jsonify
import re

ALLOWED_COUNTRIES = [
    "Afganistán", "Islas Åland", "Albania", "Argelia", "Samoa Americana", "Andorra", "Angola", "Anguila", "Antártida", "Antigua y Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaiyán", "Bahamas", "Baréin", "Bangladés", "Barbados", "Bielorrusia", "Bélgica", "Belice", "Benín", "Bermudas", "Bután", "Bolivia", "Bonaire, San Eustaquio y Saba", "Bosnia y Herzegovina", "Botsuana", "Isla Bouvet", "Brasil", "Territorio Británico del Océano Índico", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Islas Caimán", "República Centroafricana", "Chad", "Chile", "China", "Isla de Navidad", "Islas Cocos (Keeling)", "Colombia", "Comoras", "Congo", "República Democrática del Congo", "Islas Cook", "Costa Rica", "Costa de Marfil", "Croacia", "Cuba", "Curazao", "Chipre", "Chequia", "Dinamarca", "Yibuti", "Dominica", "República Dominicana", "Ecuador", "Egipto", "El Salvador", "Guinea Ecuatorial", "Eritrea", "Estonia", "Esuatini", "Etiopía", "Islas Malvinas", "Islas Feroe", "Fiyi", "Finlandia", "Francia", "Guayana Francesa", "Polinesia Francesa", "Territorios Australes Franceses", "Gabón", "Gambia", "Georgia", "Alemania", "Ghana", "Gibraltar", "Grecia", "Groenlandia", "Granada", "Guadalupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bisáu", "Guyana", "Haití", "Islas Heard y McDonald", "Santa Sede", "Honduras", "Hong Kong", "Hungría", "Islandia", "India", "Indonesia", "Irán", "Irak", "Irlanda", "Isla de Man", "Israel", "Italia", "Jamaica", "Japón", "Jersey", "Jordania", "Kazajistán", "Kenia", "Kiribati", "Corea del Norte", "Corea del Sur", "Kuwait", "Kirguistán", "Laos", "Letonia", "Líbano", "Lesoto", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Macao", "Macedonia del Norte", "Madagascar", "Malaui", "Malasia", "Maldivas", "Malí", "Malta", "Islas Marshall", "Martinica", "Mauritania", "Mauricio", "Mayotte", "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montenegro", "Montserrat", "Marruecos", "Mozambique", "Birmania", "Namibia", "Nauru", "Nepal", "Países Bajos", "Nueva Caledonia", "Nueva Zelanda", "Nicaragua", "Níger", "Nigeria", "Niue", "Isla Norfolk", "Islas Marianas del Norte", "Noruega", "Omán", "Pakistán", "Palaos", "Palestina", "Panamá", "Papúa Nueva Guinea", "Paraguay", "Perú", "Filipinas", "Islas Pitcairn", "Polonia", "Portugal", "Puerto Rico", "Catar", "Reunión", "Rumanía", "Rusia", "Ruanda", "San Bartolomé", "Santa Elena, Ascensión y Tristán de Acuña", "San Cristóbal y Nieves", "Santa Lucía", "San Martín", "San Pedro y Miquelón", "San Vicente y las Granadinas", "Samoa", "San Marino", "Santo Tomé y Príncipe", "Arabia Saudita", "Senegal", "Serbia", "Seychelles", "Sierra Leona", "Singapur", "Sint Maarten", "Eslovaquia", "Eslovenia", "Islas Salomón", "Somalia", "Sudáfrica", "Georgia del Sur y las Islas Sandwich del Sur", "Sudán del Sur", "España", "Sri Lanka", "Sudán", "Surinam", "Svalbard y Jan Mayen", "Suecia", "Suiza", "Siria", "Taiwán", "Tayikistán", "Tanzania", "Tailandia", "Timor Oriental", "Togo", "Tokelau", "Tonga", "Trinidad y Tobago", "Túnez", "Turquía", "Turkmenistán", "Islas Turcas y Caicos", "Tuvalu", "Uganda", "Ucrania", "Emiratos Árabes Unidos", "Reino Unido", "Estados Unidos", "Uruguay", "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Islas Vírgenes Británicas", "Islas Vírgenes de los Estados Unidos", "Wallis y Futuna", "Sáhara Occidental", "Yemen", "Zambia", "Zimbabue"
]
class CreateManufacturers(BaseCommand):
    
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        
        if (self.data['name'] == '' or self.data['country'] == '' or self.data['contact'] == '' or self.data['telephone'] == '' or self.data['email'] == ''):
            raise InvalidData
        
        if not self.check_name(self.data['name']):
            raise InvalidName
        
        if not self.check_country(self.data['country']):
            raise InvalidCountry
        
        if not self.check_contact(self.data['contact']):
            raise InvalidContact
        
        if not self.check_telephone(self.data['telephone']):
            raise InvalidTelephone
        
        if not self.check_email(self.data['email']):
            raise InvalidEmail

        manufacturers = Manufacturers(
            name=self.data['name'],
            country=self.data['country'],
            contact=self.data['contact'],
            telephone=self.data['telephone'],
            email=self.data['email']
        )
        db_session.add(manufacturers)

        db_session.commit()
        manufacturer_id = str(manufacturers.id)
        db_session.remove()

        return {
            'id': manufacturer_id,
            'message': 'manufacturers created successfully'
            }

    def check_name(self, name: str):
        if len(name) < 3 or len(name) > 100:
            return False
        if not re.match(r'^[\w\s\-.áéíóúÁÉÍÓÚñÑ]+$', name, re.UNICODE):
            return False
        existing_manufacturer = db_session.query(Manufacturers).filter_by(name=name).first()
        if existing_manufacturer:
            raise ExistingManufacturer
        return True

    def check_country(self, country: str):
        return country in ALLOWED_COUNTRIES
    
    def check_contact(self, contact: str):
        if len(contact) < 3 or len(contact) > 100:
            return False
        if not re.match(r'^[\w\s\-.áéíóúÁÉÍÓÚñÑ]+$', contact, re.UNICODE):
            return False
        return True

    def check_telephone(self, telephone: str):
        if len(telephone) < 7 or len(telephone) > 15:
            return False
        if not re.match(r'^\d+$', telephone):
            return False
        return True
    
    def check_email(self, email:str):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False
        return True
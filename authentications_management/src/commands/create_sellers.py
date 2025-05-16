from .base_command import BaseCommand
from ..errors.errors import *
from ..models.sellers import Sellers
from ..models.database import db_session
from .create_users import CreateUsers
from flask import jsonify
import re
import random
from datetime import datetime
import uuid


ALLOWED_COUNTRIES = [
    "Afganistán", "Islas Åland", "Albania", "Argelia", "Samoa Americana", "Andorra", "Angola", "Anguila", "Antártida", "Antigua y Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaiyán", "Bahamas", "Baréin", "Bangladés", "Barbados", "Bielorrusia", "Bélgica", "Belice", "Benín", "Bermudas", "Bután", "Bolivia", "Bonaire, San Eustaquio y Saba", "Bosnia y Herzegovina", "Botsuana", "Isla Bouvet", "Brasil", "Territorio Británico del Océano Índico", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Islas Caimán", "República Centroafricana", "Chad", "Chile", "China", "Isla de Navidad", "Islas Cocos (Keeling)", "Colombia", "Comoras", "Congo", "República Democrática del Congo", "Islas Cook", "Costa Rica", "Costa de Marfil", "Croacia", "Cuba", "Curazao", "Chipre", "Chequia", "Dinamarca", "Yibuti", "Dominica", "República Dominicana", "Ecuador", "Egipto", "El Salvador", "Guinea Ecuatorial", "Eritrea", "Estonia", "Esuatini", "Etiopía", "Islas Malvinas", "Islas Feroe", "Fiyi", "Finlandia", "Francia", "Guayana Francesa", "Polinesia Francesa", "Territorios Australes Franceses", "Gabón", "Gambia", "Georgia", "Alemania", "Ghana", "Gibraltar", "Grecia", "Groenlandia", "Granada", "Guadalupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bisáu", "Guyana", "Haití", "Islas Heard y McDonald", "Santa Sede", "Honduras", "Hong Kong", "Hungría", "Islandia", "India", "Indonesia", "Irán", "Irak", "Irlanda", "Isla de Man", "Israel", "Italia", "Jamaica", "Japón", "Jersey", "Jordania", "Kazajistán", "Kenia", "Kiribati", "Corea del Norte", "Corea del Sur", "Kuwait", "Kirguistán", "Laos", "Letonia", "Líbano", "Lesoto", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Macao", "Macedonia del Norte", "Madagascar", "Malaui", "Malasia", "Maldivas", "Malí", "Malta", "Islas Marshall", "Martinica", "Mauritania", "Mauricio", "Mayotte", "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montenegro", "Montserrat", "Marruecos", "Mozambique", "Birmania", "Namibia", "Nauru", "Nepal", "Países Bajos", "Nueva Caledonia", "Nueva Zelanda", "Nicaragua", "Níger", "Nigeria", "Niue", "Isla Norfolk", "Islas Marianas del Norte", "Noruega", "Omán", "Pakistán", "Palaos", "Palestina", "Panamá", "Papúa Nueva Guinea", "Paraguay", "Perú", "Filipinas", "Islas Pitcairn", "Polonia", "Portugal", "Puerto Rico", "Catar", "Reunión", "Rumanía", "Rusia", "Ruanda", "San Bartolomé", "Santa Elena, Ascensión y Tristán de Acuña", "San Cristóbal y Nieves", "Santa Lucía", "San Martín", "San Pedro y Miquelón", "San Vicente y las Granadinas", "Samoa", "San Marino", "Santo Tomé y Príncipe", "Arabia Saudita", "Senegal", "Serbia", "Seychelles", "Sierra Leona", "Singapur", "Sint Maarten", "Eslovaquia", "Eslovenia", "Islas Salomón", "Somalia", "Sudáfrica", "Georgia del Sur y las Islas Sandwich del Sur", "Sudán del Sur", "España", "Sri Lanka", "Sudán", "Surinam", "Svalbard y Jan Mayen", "Suecia", "Suiza", "Siria", "Taiwán", "Tayikistán", "Tanzania", "Tailandia", "Timor Oriental", "Togo", "Tokelau", "Tonga", "Trinidad y Tobago", "Túnez", "Turquía", "Turkmenistán", "Islas Turcas y Caicos", "Tuvalu", "Uganda", "Ucrania", "Emiratos Árabes Unidos", "Reino Unido", "Estados Unidos", "Uruguay", "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Islas Vírgenes Británicas", "Islas Vírgenes de los Estados Unidos", "Wallis y Futuna", "Sáhara Occidental", "Yemen", "Zambia", "Zimbabue"
]
class CreateSellers(BaseCommand):
    def __init__(self, data):
        self.data = data

    
    def execute(self):
        if (self.data['name'] == '' or self.data['country'] == '' or self.data['identification'] == '' or self.data['address'] == '' or self.data['telephone'] == '' or self.data['email'] == '' ):
            raise InvalidData
        
        if self.check_identification(self.data['identification']) == False:
            raise InvalidIdentification
        
        if self.check_name(self.data['name']) == False:
            raise InvalidName

        if not self.check_country(self.data['country']):
            raise InvalidCountry
        
        if not self.check_address(self.data['address']):
            raise InvalidAddress
        
        if not self.check_telephone(self.data['telephone']):
            raise InvalidTelephone


        if not self.check_email(self.data['email']):
            raise InvalidEmail

        seller = Sellers(
            identification=self.data['identification'],
            name=self.data['name'], 
            country=self.data['country'], 
            address=self.data['address'], 
            telephone=self.data['telephone'], 
            email=self.data['email']
        )

        identification = self.data['identification']

        password: str = f'{identification}@Pass'
        data = {
            "email": self.data['email'],
            "password": password,
            "confirm_password": password,
            "role": "Vendedor"
        }

        user_seller = CreateUsers(data).execute()
        if user_seller['message'] == 'Usuario enviado a la cola exitosamente':
            db_session.add(seller)
            db_session.commit()
            return {
                'id': f"{seller.id}",
                'message': 'Seller has been created successfully'
                }
    
    def check_identification(self, identification: str):
        if len(identification) < 6 or len(identification) > 20:
            return False
        existing_seller = db_session.query(Sellers).filter_by(identification=identification).first()
        if existing_seller:
            raise ExistingSeller
        if not re.match(r'^[a-zA-Z0-9]+$', identification):
            return False
        return True
    def check_name(self, name: str):
        if len(name) < 3 or len(name) > 100:
            return False
        if not re.match(r'^[\w\s\-.áéíóúÁÉÍÓÚñÑ]+$', name, re.UNICODE):
            return False
        return True
    def check_country(self, country: str):
        return country in ALLOWED_COUNTRIES
    def check_address(self, address: str):
        if len(address) < 10 or len(address) > 200:
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
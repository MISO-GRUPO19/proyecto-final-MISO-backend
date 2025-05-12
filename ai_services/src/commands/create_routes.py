from dotenv import load_dotenv
import re
import requests
from .base_command import BaseCommand
from ..errors.errors import InvalidData, InvalidDate
from ..models.routes import Routes
from ..models.database import db_session
import os
import random
import datetime
from datetime import datetime

load_dotenv()

load_dotenv('../.env.development')

class CreatRoute(BaseCommand):
    def __init__(self, data, token):
        self.data = data
        self.token = token
    
    def validate_date(self):
         try:
            delivery_date = datetime.strptime(self.data['date'], "%d/%m/%Y").date()
            today = datetime.now().date()
            if delivery_date < today:
                raise InvalidDate("The provided date cannot be in the past.")
         except ValueError:
            raise InvalidDate("The provided date format is invalid. Use 'dd/MM/yyyy'.")


    def execute(self):
        if (self.data['date'] == ''):
            raise InvalidData
        
        self.validate_date()

        
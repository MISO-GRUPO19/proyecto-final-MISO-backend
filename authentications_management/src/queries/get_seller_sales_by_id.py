from ..errors.errors import *
from ..models.sellers import Sellers, GoalProduct, Goals
from ..models.database import db_session
from flask import jsonify
import re
import random
from datetime import datetime
import uuid
from sqlalchemy import extract, func, cast, String



class GetSellerSalesById():
    def __init__(self, seller_identification):
        self.seller_identification = seller_identification
    
    def validate_name(self):
        
        if self.seller_identification.isdigit():
            seller = db_session.query(Sellers).filter(Sellers.identification == self.seller_identification).first()
        else:
        # Otherwise, treat it as a name
            seller = db_session.query(Sellers).filter(Sellers.name == self.seller_identification).first()

        if not seller:
            raise SellerNotFound
    
        return seller

    def execute(self):

        seller: Sellers = self.validate_name()
        
        try:
            goals = db_session.query(Goals).filter(Goals.seller_id == seller.id).all()
            if not goals:
                raise GoalNotFound
            monthly_summary = []
            total_seller_sales = 0
            for goal in goals:
                monthly_sales = 0
                monthly_expecation = 0
                product_goals = db_session.query(GoalProduct).filter(GoalProduct.goal_id == goal.id).all()
                for row in product_goals:
                    total_seller_sales += row.sales
                    monthly_sales += row.sales
                    monthly_expecation += row.sales_expectation
                    date = row.date.strftime("%m-%Y")
                goals_achieved = round((monthly_sales / monthly_expecation) * 100, 2) if monthly_expecation > 0 else 0
                monthly_summary.append({
                    "date": date,  
                    "total_sales": monthly_sales,
                    "goals": monthly_expecation,
                    "goals_achieved": goals_achieved  
                })
                
            seller_data = {
                "name" : f"{seller.name}",
                "country": f"{seller.country}",
                "phone": f"{seller.telephone}",
                "email": f"{seller.email}",
                "total_sales": total_seller_sales,
                "monthly_summary": monthly_summary
            }
            
            return seller_data, 200
        except Exception as e:
            raise e



    
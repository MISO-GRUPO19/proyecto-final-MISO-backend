from .base_queries import BaseQueries
from ..models.products import Category
from ..models.database import db_session

class GetCategories(BaseQueries):
    def __init__(self, token):
        self.token = token

    def execute(self):
        try:

            GetCategories = db_session.query(Category).all()

            category_list = []
            for category in GetCategories:
                category_list.append({
                    'id': category.id,
                    'name': category.name
                })

            return category_list

        except Exception as e:
            return {'error': str(e)}
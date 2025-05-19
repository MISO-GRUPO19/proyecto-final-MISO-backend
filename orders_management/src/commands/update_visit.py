from datetime import datetime
from ..errors.errors import InvalidData
from ..models.visits import Visits
from ..models.database import db_session

class UpdateVisit:
    VALID_STATES = ['VISITADO', 'NO_VISITADO']

    def __init__(self, token, visit_id, new_state):
        self.token = token
        self.visit_id = visit_id
        self.new_state = new_state

    def execute(self):
        if self.new_state not in self.VALID_STATES:
            raise InvalidData

        with db_session() as session:
            visit = session.query(Visits).filter(Visits.id == self.visit_id).first()
            
            if not visit:
                raise InvalidData("Visit not found")
        

            visit.visit_status = self.new_state
            visit.visit_date = datetime.now()
            
            try:
                session.commit()
            except Exception as e:
                raise Exception("Database error") from e

        return {"message": f"Visit {self.visit_id} updated to {self.new_state}"}
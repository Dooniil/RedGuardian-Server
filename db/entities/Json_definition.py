from sqlalchemy import Column, JSON, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel
from db.entities.Family import Family


class JsonDefinition(async_db_session.base, BehaviorModel):
    __tablename__ = 'json_definition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    family_id = Column(Integer, ForeignKey('family.id'), nullable=False)
    description = Column(String, nullable=True)
    json_format = Column(JSON, nullable=False)

    @property
    def repr(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'json_format': self.json_format
        }
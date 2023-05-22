from sqlalchemy import Column, JSON, Integer, String, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


class JsonDefinition(async_db_session.base, BehaviorModel):
    __tablename__ = 'json_definition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    family = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    json_format = Column(JSON, nullable=False)
    execute_definition = relationship('ExecDefinition', uselist=False, back_populates='json_definition')
    
    @property
    def repr(self):
        return {
            'id': self.id,
            'title': self.title,
            'family_id': self.family,
            'description': self.description,
            'json_format': self.json_format,
            'execute_definition': self.execute_definition
        }


class ExecDefinition(async_db_session.base, BehaviorModel):
    __tablename__ = 'execute_definition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    json_definition_id = Column(Integer, ForeignKey("json_definition.id"), nullable=False)
    json_definition = relationship(JsonDefinition, uselist=False, back_populates='execute_definition')
    type_def = Column(Integer, nullable=False)
    family = Column(Integer, nullable=False)
    scripts = Column(ARRAY(JSON), nullable=True)


    @property
    def repr(self):
        return {
            'id': self.id,
            'json_definition_id': self.json_definition_id,
            'family_id': self.family,
            'type_def': self.type_def,
            'scripts': self.scripts
        }
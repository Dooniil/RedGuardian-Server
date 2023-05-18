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


class ExecDefinition(async_db_session.base, BehaviorModel):
    __tablename__ = 'execute_definition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    json_definition_id = Column(Integer, ForeignKey("json_definition.id"), nullable=False)
    json_definition = relationship(JsonDefinition, uselist=False, backref='execute_definition')
    family_id = Column(Integer, ForeignKey('family.id'), nullable=False)
    os_check = Column(JSON)
    vuln_check = Column(JSON)


    @property
    def repr(self):
        return {
            'id': self.id,
            'json_definition_id': self.json_definition_id,
            'family_id': self.family_id,
            'os_check': self.os_check,
            'vuln_check': self.vuln_check
        }
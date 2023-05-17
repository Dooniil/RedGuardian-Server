from sqlalchemy import Column, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel
from db.entities.Family import Family


class ExecDefinition(async_db_session.base, BehaviorModel):
    __tablename__ = 'execute_definition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    json_definition_id = Column(Integer, ForeignKey("json_definition.id"), nullable=False)
    family_id = Column(Integer, ForeignKey('family.id'), nullable=False)
    os_check = Column(JSON)
    vuln_check = Column(JSON)
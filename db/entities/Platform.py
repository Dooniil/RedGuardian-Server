from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


class Platform(async_db_session.base, BehaviorModel):
    __tablename__ = 'platform'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    # credentials = relationship('Credential', back_populates="platform")

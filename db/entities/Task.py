from sqlalchemy import Column, Boolean, DateTime, Integer, String, ForeignKey, JSON, func
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


class Task(async_db_session.base, BehaviorModel):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    credential_id = Column(Integer, ForeignKey('credential.id'), nullable=True)
    scanner_id = Column(Integer, ForeignKey('scanner.id'), nullable=False)
    task_type = Column(Integer, nullable=False)
    custom_settings = Column(JSON, nullable=False)
    run_after_creation = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    @property
    def repr(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'credential_id': self.credential_id,
            'scanner_id': self.scanner_id,
            'type': self.task_type,
            'custom_settings': self.custom_settings,
            'run_after_creation': self.run_after_creation,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    async def get_filter(cls, *args):
        pass

from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


class ScanResult(async_db_session.base, BehaviorModel):
    __tablename__ = 'scan_result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_result_id = Column(Integer, ForeignKey('task_result.id'), nullable=False)
    task_result = relationship('TaskResult', back_populates='scan_results')
    host_id = Column(Integer, ForeignKey('host.id'), nullable=True)
    custom_result = Column(JSON, nullable=False)

    @property
    def repr(self):
        return {
            'id': self.id,
            'task_result_id': self.task_result_id,
            'host_id': self.host_id,
            'custom_result': self.custom_result,
        }

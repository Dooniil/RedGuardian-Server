from sqlalchemy import Column, DateTime, Time, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


class TaskResult(async_db_session.base, BehaviorModel):
    __tablename__ = 'task_result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    scan_results = relationship('ScanResult', back_populates='task_result')
    exec_time = Column(Time, nullable=True)
    start_at = Column(DateTime(timezone=False), nullable=True)
    end_at = Column(DateTime(timezone=False), nullable=True)

    @property
    def repr(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'scan_results': self.scan_results,
            'exec_time': self.exec_time,
            'start_at': self.start_at,
            'end_at': self.end_at
        }

from sqlalchemy import Column, Integer, String, DateTime, Boolean, select
from sqlalchemy.sql import func
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


class Scanner(async_db_session.base, BehaviorModel):
    __tablename__ = 'scanner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(50), nullable=False)
    port = Column(Integer, default=8084, nullable=False)
    description = Column(String, nullable=True)
    in_use = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    @property
    def repr(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'port': self.port,
            'in_use': self.in_use,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    async def get_in_use(cls):
        stmt = select(cls).where(cls.in_use == True)
        result = await async_db_session.execute(stmt)
        return result.all()

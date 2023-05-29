from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, select
from sqlalchemy.sql import func, cast
from sqlalchemy.orm import relationship
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


class Credential(async_db_session.base, BehaviorModel):
    __tablename__ = 'credential'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    login = Column(LargeBinary, nullable=False)
    password = Column(LargeBinary, nullable=False)
    family = Column(Integer, nullable=False)
    # platform = relationship('Platform', back_populates="credentials")
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    @property
    def repr(self):
        return {
            'id': self.id,
            'name': self.name,
            'login': self.login,
            'password': self.password,
            'family': self.family,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    async def get_filter(cls, name: str,
                         family_id: int
                         ):
        if family_id == 0:
            stmt = select(cls).where(
                cls.name.ilike(f'{name}%')
            )
        else:
            stmt = select(cls).where(
                (cls.name.ilike(f'{name}%')) &
                (cls.family == family_id)
            )
        result = await async_db_session.execute(stmt)
        return result.all()

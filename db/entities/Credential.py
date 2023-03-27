from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, ForeignKey, LargeBinary, select
from sqlalchemy.sql import func, cast
from sqlalchemy.orm import relationship
from db.database import async_db_session
from db.entities.Platform import Platform
from db.entities.behavior_model import BehaviorModel


class Credential(async_db_session.base, BehaviorModel):
    __tablename__ = 'credential'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    login = Column(String(100), nullable=False)
    password = Column(LargeBinary, nullable=False)
    platform_id = Column(Integer, ForeignKey('platform.id'), nullable=False)
    platform = relationship('Platform', back_populates="credentials")
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    @property
    def repr(self):
        return {
            'id': {self.id},
            'name': {self.name},
            'login': self.login,
            'password': 'encrypted',
            'platform_id': {self.platform_id},
            'created_at': {self.created_at},
            'updated_at': {self.updated_at}
        }

    @classmethod
    async def get_filter(cls, name: str,
                         platform_id: int,
                         created_at: str,
                         updated_at: str
                         ):
        if platform_id == 0:
            stmt = select(cls).where(
                (cls.name.ilike(f'{name}%'))
                # (cls.created_at >= created_at) &
                # (cls.updated_at >= updated_at)
            )
        else:
            stmt = select(cls).where(
                (cls.name.ilike(f'{name}%')) &
                (cls.platform_id == platform_id)
                # (cls.created_at >= created_at) &
                # (cls.updated_at >= updated_at)
            )
        result = await async_db_session.execute(stmt)
        return result.all()

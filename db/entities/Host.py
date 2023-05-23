from sqlalchemy import Column, String, DateTime, Integer, select, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import async_db_session
from db.entities.behavior_model import BehaviorModel


GroupsHosts = Table('GroupsHosts', async_db_session.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('group_id', ForeignKey('group_hosts.id')),
    Column('host_id', ForeignKey('host.id')),
)


class GroupHosts(async_db_session.base, BehaviorModel):
    __tablename__ = 'group_hosts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    hosts = relationship('Host', secondary='GroupsHosts', back_populates='groups')
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    @property
    def repr(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'hosts': self.hosts,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Host(async_db_session.base, BehaviorModel):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String, nullable=True, unique=True)
    description = Column(String, nullable=True)
    dns = Column(String, nullable=True, unique=True)
    family = Column(Integer, nullable=True)
    cpe = Column(String, nullable=True)
    groups = relationship('GroupHosts', secondary='GroupsHosts', back_populates='hosts')
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    @property
    def repr(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'description': self.description,
            'dns': self.dns,
            'family': self.family,
            'cpe': self.cpe,
            'groups': self.groups,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    async def get_host_by_ip(cls, ip):
        stmt = select(cls).where(cls.ip.ilike(ip))
        result = await async_db_session.execute(stmt)
        return result.first()

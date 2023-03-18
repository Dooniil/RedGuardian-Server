from sqlalchemy import select, delete
from db.database import async_db_session


class BehaviorModel:
    @classmethod
    async def create(cls, **kwargs):
        instance = cls(**kwargs)
        async_db_session.add(instance)

        try:
            await async_db_session.commit()
        except Exception:
            await async_db_session.rollback()
            raise
        return instance

    @classmethod
    async def get(cls, pk):
        stmt = select(cls).where(cls.id == pk)
        result = await async_db_session.execute(stmt)
        return result.first()

    @classmethod
    async def get_all(cls):
        stmt = select(cls)
        instances = await async_db_session.execute(stmt).all()
        return instances

    @classmethod
    async def delete(cls, pk):
        stmt = delete(cls).where(cls.id == pk)
        await async_db_session.execute(stmt)
        try:
            await async_db_session.commit()
        except Exception:
            await async_db_session.rollback()
            raise

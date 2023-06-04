from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload

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
        return result.first()[0]

    @classmethod
    async def get_by_name(cls, name: str):
        stmt = select(cls).where(cls.name.ilike(name))
        result = await async_db_session.execute(stmt)
        return result.first()

    @classmethod
    async def get_all(cls):
        stmt = select(cls)
        result = await async_db_session.execute(stmt)
        return result.all()

    @classmethod
    async def delete(cls, pk):
        stmt = delete(cls).where(cls.id == pk)
        await async_db_session.execute(stmt)
        try:
            await async_db_session.commit()
        except Exception:
            await async_db_session.rollback()
            raise

    @classmethod
    async def update(cls, pk, new_data: dict):
        stmt = update(cls).where(cls.id == pk).values(**new_data)
        await async_db_session.execute(stmt)
        try:
            await async_db_session.commit()
        except Exception:
            await async_db_session.rollback()
            raise

    @classmethod
    async def get_relationship(cls, id, relationship):
        try:
            stmt = select(cls).where(cls.id == id).options(selectinload(relationship))
            result = await async_db_session.execute(stmt)
            instance = result.scalars().one()
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}

        return instance

    
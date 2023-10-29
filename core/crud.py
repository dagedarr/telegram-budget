from typing import TypeVar

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


async def get_by_id(
    model: ModelType,
    obj_id: int,
    session: AsyncSession
):
    """Получение объекта по id."""
    get_obj_in_db = await session.execute(
        select(model).where(model.id == obj_id)
    )
    return get_obj_in_db.scalars().first()


async def get_or_create(
    session: AsyncSession,
    model: ModelType,
    **kwargs
):
    """Получение или создание объекта."""
    instance = await session.execute(select(model).filter_by(**kwargs))
    instance = instance.scalars().one_or_none()

    if not instance:
        instance = await session.execute(insert(model).values(**kwargs))
        await session.commit()
    return instance


async def update(
    db_obj: ModelType,
    obj_in: dict,
    session: AsyncSession,
) -> ModelType:
    """Изменение значений полей объекта."""
    for field in obj_in:
        setattr(db_obj, field, obj_in[field])
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def create(
    session: AsyncSession,
    model: ModelType,
    **kwargs
):
    """Создание объекта."""
    await session.execute(insert(model).values(**kwargs))
    await session.commit()

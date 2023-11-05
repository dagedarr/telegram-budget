from typing import Optional, TypeVar

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


async def get_by_id(
    model: ModelType,
    obj_id: int,
    session: AsyncSession
) -> ModelType:
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
    flag = True

    if not instance:
        instance = await session.execute(insert(model).values(**kwargs))
        await session.commit()
        flag = False
    return instance, flag


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
    """Создание объекта и возвращает его."""

    new_object = model(**kwargs)
    session.add(new_object)
    await session.commit()
    await session.refresh(new_object)
    return new_object


async def get_by_attributes(
    model: ModelType,
    attributes: dict,
    session: AsyncSession,
    get_multi: bool = False,
    amount: Optional[int] = None,
    order_by: Optional[str] = None
):
    """Получение объекта/объектов по нескольким атрибутам."""

    query = select(model).where(
        *[
            getattr(model, attr_name) == attr_value
            for attr_name, attr_value in attributes.items()
        ]
    )

    if order_by is not None:
        query = query.order_by(getattr(model, order_by).desc())

    if not get_multi:
        get_obj_in_db = await session.execute(query)
        return get_obj_in_db.scalars().first()

    if amount is not None:
        query = query.limit(amount)

    get_objs_in_db = await session.execute(query)
    return get_objs_in_db.scalars().all()


async def remove(
    db_obj: ModelType,
    session: AsyncSession,
) -> ModelType:
    """Удаление объекта."""

    await session.delete(db_obj)
    await session.commit()
    return db_obj

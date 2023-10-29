from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class Category(Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(64), nullable=False)

    user = relationship('User', back_populates='categories')
    aliases = relationship(
        'Alias', back_populates='category', cascade='all, delete-orphan'
    )
    # transactions = relationship('Transaction', back_populates='category')


class Alias(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    title = Column(String(64), nullable=False)

    user = relationship('User', back_populates='aliases')
    category = relationship('Category', back_populates='aliases')

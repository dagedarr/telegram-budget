from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class Category(Base):
    """Модель Категории пользователя."""

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(64), nullable=False)

    user = relationship('User', back_populates='categories')
    aliases = relationship(
        'Alias', back_populates='category', cascade='all, delete-orphan', lazy='selectin'
    )
    transactions = relationship(
        'Transaction', back_populates='category', cascade='all, delete-orphan', lazy='selectin'
    )

    def __str__(self) -> str:
        return str(self.title)

    def __repr__(self) -> str:
        return str(self.title)


class Alias(Base):
    """Модель Алиаса категории."""

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    title = Column(String(64), nullable=False)

    user = relationship('User', back_populates='aliases')
    category = relationship(
        'Category', back_populates='aliases', lazy='selectin')
    transactions = relationship(
        'Transaction', back_populates='alias', lazy='selectin')

    def __str__(self) -> str:
        return f'{self.title} ({self.category})'

    def __repr__(self) -> str:
        return f'{self.title} ({self.category})'

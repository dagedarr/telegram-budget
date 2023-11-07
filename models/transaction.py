from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.db import Base


class Transaction(Base):
    """Модель Транзакции пользователя."""

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    alias_id = Column(Integer, ForeignKey('alias.id'))

    amount = Column(Float, nullable=False)
    date = Column(BigInteger)

    user = relationship('User', back_populates='transactions')
    category = relationship(
        'Category', back_populates='transactions', lazy='selectin'
    )

    alias = relationship(
        'Alias', back_populates='transactions', lazy='selectin'
    )

    def __str__(self) -> str:
        if self.alias:
            return f'{self.amount} -> {self.alias}'
        return f'{self.amount} -> {self.category}'

    def __repr__(self) -> str:
        if self.alias:
            return f'{self.amount} -> {self.alias}'
        return f'{self.amount} -> {self.category}'

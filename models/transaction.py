from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.db import Base


class Transaction(Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(BigInteger)

    user = relationship('User', back_populates='transactions')
    # category = relationship('Category', back_populates='transactions')

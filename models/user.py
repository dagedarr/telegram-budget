from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship

from core.db import Base


class User(Base):
    """Модель пользователя"""

    username = Column(String(64), nullable=True)
    email = Column(String(254), unique=True, index=True, nullable=True)
    registration_time = Column(BigInteger)  # Время в формате Unix.
    is_onboarding = Column(Boolean, default=False)

    categories = relationship('Category', back_populates='user')
    aliases = relationship('Alias', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')

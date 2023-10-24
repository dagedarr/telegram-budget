from sqlalchemy import BigInteger, Boolean, Column, String, Text

from core.db import Base


class User(Base):
    """Модель пользователей"""
    username = Column(String(64), nullable=True)
    email = Column(String(254), unique=True, index=True, nullable=True)
    # Время в формате Unix.
    registration_time = Column(BigInteger)
    is_onboarding = Column(Boolean, default=False)

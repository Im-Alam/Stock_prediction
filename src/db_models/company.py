from src.db_models.model import Base
from typing import List, Optional
from sqlalchemy import Integer, Enum, BIGINT, String, ForeignKey, DateTime, func, or_, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse


class Company(Base):
    __tablename__='company_table'
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol : Mapped[str] = mapped_column(String, nullable=True, unique=True)
    company_name : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    mcap : Mapped[int] = mapped_column(BIGINT, nullable = True)
    sector : Mapped[str] = mapped_column(String, nullable=True)
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


    comment = relationship('Comment', back_populates='user', cascade="all, delete-orphan")
    event = relationship('Event', back_populates='company', cascade='all, delete-orphan')
    news_l = relationship('News', secondary='news_company_association', back_populates='companies')

    
    def __repr__(self) -> str:
        return f'{self.id} : {self.company_name}'
    
    
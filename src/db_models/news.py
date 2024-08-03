from src.db_models.model import Base
from typing import List, Optional
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, or_, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse

class NewsCompanyAssociation(Base):
    __tablename__ = 'news_company_association'
    news_id = Mapped[int] = mapped_column(ForeignKey('News.id'), primary_key=True)
    company_id = Mapped[int] = mapped_column(ForeignKey('Company.id'), primary_key=True)
    relevance_score = Mapped[Optional[Numeric]]
    sentiment_score = Mapped[Optional[Numeric]]
    

class News(Base):
    __tablename__ = 'news'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String(100), nullable = False )
    content: Mapped[str] = mapped_column(Text, nullable = True )
    company_tag = Mapped[Optional[str]] = mapped_column(ForeignKey('Company.id'))
    topic: Mapped[str]
    news_url: Mapped[str] = mapped_column(String, nullable=False)
    sentiment:Mapped[int] = mapped_column(Integer, nullable=False)
    sentiment_statement: Mapped[str] = mapped_column(String, nullable = True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    companies = relationship('Company', secondary='news_company_association', back_populates='news_l')

    

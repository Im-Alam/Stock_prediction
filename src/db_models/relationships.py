from src.db_models.base import Base
from typing import List, Optional
from sqlalchemy import Integer, Enum, ForeignKey, DateTime, func, or_, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session



class CommentCompanyAssociation(Base):
    __tablename__ = 'comment_company_association'
    comment_id: Mapped[int] = mapped_column(ForeignKey('user_comment.id', ondelete='CASCADE'), primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('company_table.id', ondelete='CASCADE'), primary_key=True)


class NewsCompanyAssociation(Base):
    __tablename__ = 'news_company_association'
    news_id : Mapped[int] = mapped_column(ForeignKey('news_table.id', ondelete='CASCADE'), primary_key=True)
    company_id : Mapped[int] = mapped_column(ForeignKey('company_table.id', ondelete='CASCADE'), primary_key=True)


    

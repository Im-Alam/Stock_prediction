from src.db_models.base import Base
from typing import List, Optional
from sqlalchemy import Integer, Enum, BIGINT, String, ForeignKey, DateTime, func, or_, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError


class Company(Base):
    __tablename__='company_table'
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol : Mapped[str] = mapped_column(String, nullable=True)
    company_name : Mapped[str] = mapped_column(String, unique=True)
    mcap : Mapped[int] = mapped_column(BIGINT, nullable = True)
    sector : Mapped[str] = mapped_column(String, nullable=True)
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    events = relationship('Event', 
                        back_populates='company', 
                        cascade='all, delete')
    news = relationship('News', 
                        secondary='news_company_association', 
                        back_populates='companies')
    comments = relationship('Comment', 
                        secondary='comment_company_association', 
                        back_populates='companies')
    
    
    def __repr__(self) -> str:
        return (f'{self.id} : {self.company_name}' if self.id and self.company_name else "<Company (no name)>")
    

    def insert_or_update_company(company_data: dict):
        """
        Inserts or updates a company entry into the company table.

        Args:
            company_data (dict): Dictionary containing company data.
        """
        # Check if the company already exists
        session = Session(engine)
        try:
            company = session.query(Company).filter_by(name=company_data["company_name"]).first()
            if company:
                # Update the existing company with new data
                if not company.symbol:
                    company.symbol = company_data.get("symbol")
                company.mcap = company_data.get("mcap")
                company.sector = company_data["sector"]

            else:
                # If the company does not exist, create a new Company object
                company = Company(
                    company_name=company_data["company_name"],
                    symbol=company_data.get("symbol"),
                    sector=company_data.get("sector"),
                    mcap = company_data["mcap"]
                )
                session.add(company)
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, "Cant insert company details")
        finally:
            session.close()

    
    
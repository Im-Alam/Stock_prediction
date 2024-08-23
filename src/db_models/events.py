from src.db_models.base import Base
from typing import List, Optional
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, or_, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy.dialects.postgresql import ENUM
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError

listing_platform_enum = ENUM('stock','ipo','general', name='listing_platform_enum')

class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    event_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company_table.id'))
    related_to: Mapped[str] = mapped_column(listing_platform_enum, default='general')
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    company = relationship('Company', back_populates='events')

    def __repr__(self) -> str:
        return f'{self.id}: {self.event_date}: {self.name}'
    
    @classmethod
    def get_ipo_event_companywise(self, companyId:int, regarding:str):
        session = Session(engine)
        try:
            return session.query(Event).filter(
                self.comapany_id == companyId,
                self.related_to == regarding
            ).all()
        except Exception as e:
            session.rollback()
            return apiError(400, f'{e}:\nError occured while retriving event detail')
        finally:
            session.close()


    @classmethod
    def get_todays_events(self):
        session = Session(engine)
        try:
            today = func.current_date()
            # return session.query(Event).filter(
            #         func.date(self.event_date) == today
            #     ).all()
        except Exception as e:
            session.rollback()
            return apiError(400, f'{e}:\nError occured while retriving current events')
        finally:
            session.close()


            
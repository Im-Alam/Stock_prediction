from src.db_models.base import Base
from sqlalchemy import insert, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError



class IndicesTable(Base):
    __tablename__ = 'Indices_table'

    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), primary_key=True)

    nifty50: Mapped[float] = mapped_column(Float, nullable=False)  # NSE NIFTY 50 (India)
    sensex: Mapped[float] = mapped_column(Float, nullable=False)  # BSE SENSEX (India)  
    bank_nifty: Mapped[float] = mapped_column(Float, nullable=False)  # Bank Nifty (India)
    nifty_auto: Mapped[float] = mapped_column(Float, nullable=False)  # Nifty Auto (India)
    nifty_it: Mapped[float] = mapped_column(Float, nullable=False)  # Nifty IT (India)
    nifty_pharma: Mapped[float] = mapped_column(Float, nullable=False)  # Nifty Pharma (India)

    dow_jones: Mapped[float] = mapped_column(Float, nullable=False)  # Dow Jones (USA)
    nasdaq: Mapped[float] = mapped_column(Float, nullable=False)  # NASDAQ (USA)
    s_and_p_500: Mapped[float] = mapped_column(Float, nullable=False)  # S&P 500 (USA)
    ftse_100: Mapped[float] = mapped_column(Float, nullable=False)  # FTSE 100 (UK)
    dax: Mapped[float] = mapped_column(Float, nullable=False)  # DAX (Germany)
    nikkei_225: Mapped[float] = mapped_column(Float, nullable=False)  # Nikkei 225 (Japan)
    shanghai_composite: Mapped[float] = mapped_column(Float, nullable=False)  # Shanghai Composite (China)

    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


    def __repr__(self) -> str:
        return (f"Indices_table(Time = {self.timestamp})")
    
    @classmethod
    def fetch_recent(cls, n:int=50):
        session = Session(engine)
        try:
            return session.query(cls).order_by(cls.timestamp.desc()).limit(n).all()
        except Exception as e:
            session.rollback()
            return apiError(400, "Error while fetching n index data")
        finally:
            session.close() 


    def insert_data(self, data_dict: dict):
        session = Session(engine)
        try:
            new_record = IndicesTable(**data_dict)
            session.add(new_record)
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, f"Error occured while inserting indivisual index data:{e}")
        finally:
            session.close()

    @classmethod
    def insert_data_bulk(cls, data_list: list):
        """
         Parameters:
        - data_list: List of dictionaries containing the data to be inserted.
        """
        try:
            session = Session(engine)
            session.execute(insert(cls), data_list)
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, f"bulk insertion into index faules with {e}")
        finally:
            session.close()

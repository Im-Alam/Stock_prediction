from src.db_models.model import Base
from typing import List, Optional
from sqlalchemy import Integer, Float, DateTime, func, or_
from sqlalchemy.orm import Mapped, mapped_column, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse



class IndicesTable(Base):
    __tablename__ = 'Indices_table'
    #collects data of trading day closing price

    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    niftyPrediction: Mapped[float] = mapped_column(Float, nullable=True)  # NSE NIFTY 50 (India)
    predictionAccuracy: Mapped[float] = mapped_column(Float, nullable=True)  # NSE NIFTY 50 (India)
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
        return (f"IndicesTable(id={self.id}, timestamp={self.timestamp}")
    

    @classmethod
    def fetch_recent_nData(cls, n):
        session = Session(engine)
        try:
            return session.query(cls).order_by(cls.timestamp.desc()).limit(n).all()
        except Exception as e:
            session.rollback()
            return apiError(400, "Error while fetching n index data")
        finally:
            session.close()


    def insert_data(data_dict: dict):
        try:
            session = Session(engine)
            new_record = IndicesTable(**data_dict)
            session.add(new_record)
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, f"Error occured while inserting index data:{e}")
        finally:
            session.close()



    def insert_data_bulk(data_list: list):
        """
         Parameters:
        - data_list: List of dictionaries containing the data to be inserted.
        """
        try:
            session = Session(engine)
            session.bulk_insert_mappings(IndicesTable, data_list)
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, f"bulk insertion into index faules with {e}")
        finally:
            session.close()

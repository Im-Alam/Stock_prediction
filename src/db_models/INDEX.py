from src.db_models.model import Base
from typing import List, Optional
from sqlalchemy import Integer, Float, DateTime, func, or_
from sqlalchemy.orm import Mapped, mapped_column, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse



class IndicesTable(Base):
    __tablename__ = 'Indices_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    sensex: Mapped[float] = mapped_column(Float, nullable=False)  # BSE SENSEX (India)
    nifty50: Mapped[float] = mapped_column(Float, nullable=False)  # NSE NIFTY 50 (India)
    niftyPrediction: Mapped[float] = mapped_column(Float, nullable=True)  # NSE NIFTY 50 (India)
    predictionAccuracy: Mapped[float] = mapped_column(Float, nullable=True)  # NSE NIFTY 50 (India)
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


    def __repr__(self) -> str:
        return (f"IndicesTable(id={self.id}, timestamp={self.timestamp}")
    
    @classmethod
    def fetch_recent_nData(cls, n):
        session = Session
        return session.query(cls).order_by(cls.timestamp.desc()).limit(n).all()
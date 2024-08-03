from src.db_models.model import Base
from typing import List, Optional
from sqlalchemy import BIGINT, ForeignKey, DateTime, func, or_, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse



class Ipo(Base):
    __tablename__ = 'ipo'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id : Mapped[int] = mapped_column(ForeignKey('Company.id'))
    registar_id: Mapped[int] = mapped_column(ForeignKey('Registrar.id'))
    min_price_per_issue: Mapped[int]
    lot_size: Mapped[int]
    offer_for_sale: Mapped[Optional[int]] = mapped_column(BIGINT)
    fresh_issue: Mapped[Optional[int]] = mapped_column(BIGINT)
    listing_platform: Mapped[str] = mapped_column(comment='Contains: NSE/BSE')
    promoter_holding_preissue: Mapped[Optional[BIGINT]]
    promoter_holding_postissue: Mapped[Optional[BIGINT]]
    promoter_share_preissue: Mapped[Optional[BIGINT]]
    about_company: Mapped[Text]
    about_ipo: Mapped[Text]
    overall_subscription: Mapped[float]
    rhp_url: Mapped[Optional[str]]
    drhp_url: Mapped[str]
    anchor_investor_url: Mapped[str]
    created_at : Mapped[DateTime] = mapped_column(default=func.now())



    def __repr__(self):
        return f'id: {self.id} Max price per issue: {self.price_band}'
    





















class Investor(Base):
    __tablename__ = 'investor_distribution'
    id: Mapped[int] = mapped_column(ForeignKey('Ipo.id'), primary_key=True)
    fii: Mapped[BIGINT] = mapped_column(comment='Issues alloted to FII')
    dii: Mapped[BIGINT] = mapped_column(comment='Issues alloted to DII')
    nii: Mapped[BIGINT] = mapped_column(comment='Issues alloted to NII')
    bnii: Mapped[BIGINT] = mapped_column(comment='Issues alloted to BNII')
    snii: Mapped[BIGINT] = mapped_column(comment='Issues alloted to SNII')
    retailer: Mapped[BIGINT] = mapped_column(comment='Issues alloted to Retailers')
    anchor: Mapped[BIGINT] = mapped_column(comment='anchor investor holdng')
    created_at : Mapped[DateTime] = mapped_column(default=func.now())


    def __repr__(self) -> str:
        return f'Invesment in company id {self.id}'



class Lot(Base):
    __tablename__= 'lot_size'
    id:Mapped[int] = mapped_column(ForeignKey('Ipo.id'), primary_key=True)
    max_price_per_issue: Mapped[int]
    lot_size: Mapped[int]
    retail_min: Mapped[int]
    retail_max: Mapped[int]
    created_at : Mapped[DateTime] = mapped_column(default=func.now())


class Registrar(Base):
    __tablename__= 'registrar'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('Company.id'))
    name: Mapped[str]
    webpage: Mapped[str]
    email:Mapped[str]
    phone:Mapped[str]
    created_at : Mapped[DateTime] = mapped_column(default=func.now())
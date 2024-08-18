from src.db_models.user import Base
from typing import List, Optional
from sqlalchemy import BIGINT, ForeignKey, DateTime, func, or_, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse



class Ipo(Base):
    __tablename__ = 'ipo_table'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id : Mapped[int] = mapped_column(ForeignKey('company_table.id'))
    registar_id: Mapped[int] = mapped_column(ForeignKey('registrar_table.id'))

    offer_for_sale: Mapped[Optional[int]] = mapped_column(BIGINT)
    fresh_issue: Mapped[Optional[int]] = mapped_column(BIGINT)
    listing_platform: Mapped[str] = mapped_column(comment='Contains: NSE/BSE')
    promoter_holding_preissue: Mapped[Optional[int]] = mapped_column(BIGINT)
    promoter_holding_postissue: Mapped[Optional[int]] = mapped_column(BIGINT)
    promoter_share_preissue: Mapped[Optional[int]] = mapped_column(BIGINT)
    about_company: Mapped[str] = mapped_column(Text)
    about_ipo: Mapped[str] = mapped_column(Text)
    overall_subscription: Mapped[float]
    rhp_url: Mapped[Optional[str]]
    drhp_url: Mapped[str]
    anchor_investor_url: Mapped[str]
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    investors: Mapped[List['Investor']] = relationship(back_populates='ipo', cascade='all, delete')
    lot: Mapped[List['Lot']] = relationship(back_populates='ipo', cascade='all, delete')
    registrar: Mapped[List['Registrar']] = relationship(back_populates='ipos')

    def __repr__(self):
        return f'<id: {self.id} Max price per issue: {self.company_id}>'
    



class Investor(Base):
    __tablename__ = 'investor_distribution'
    id: Mapped[int] = mapped_column(ForeignKey('ipo_table.id'), primary_key=True)
    fii: Mapped[int] = mapped_column(BIGINT, comment='Issues alloted to FII')
    dii: Mapped[int] = mapped_column(BIGINT, comment='Issues alloted to DII')
    nii: Mapped[int] = mapped_column(BIGINT, comment='Issues alloted to NII')
    bnii: Mapped[int] = mapped_column(BIGINT, comment='Issues alloted to BNII')
    snii: Mapped[int] = mapped_column(BIGINT, comment='Issues alloted to SNII')
    retailer: Mapped[int] = mapped_column(BIGINT, comment='Issues alloted to Retailers')
    anchor: Mapped[int] = mapped_column(BIGINT, comment='anchor investor holdng')
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    ipo: Mapped['Ipo'] = relationship(back_populates='investors')

    def __repr__(self) -> str:
        return f'Invesment in company id {self.id}'



class Lot(Base):
    __tablename__= 'lot_size_table'
    id:Mapped[int] = mapped_column(ForeignKey('ipo_table.id'), primary_key=True)
    min_price_per_issue: Mapped[int]
    max_price_per_issue: Mapped[int]
    lot_size: Mapped[int]
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    ipo: Mapped['Ipo'] = relationship( back_populates='lot')

    def __repr__(self) -> str:
        return f'Price band: [{self.min_price_per_issue}-{self.max_price_per_issue}]'

class Registrar(Base):
    __tablename__= 'registrar_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('company_table.id'))
    name: Mapped[str]
    webpage: Mapped[str]
    email:Mapped[str]
    phone:Mapped[str]
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    ipos: Mapped['Ipo'] = relationship(back_populates='registrar')
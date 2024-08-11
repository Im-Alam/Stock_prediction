from db_models.user import Base
from typing import List, Optional
from sqlalchemy import Integer, Float, DateTime, func, or_
from sqlalchemy.orm import Mapped, mapped_column, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse



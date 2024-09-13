from src.db_models.base import Base
from src.db_models.user import User
from src.db_models.feedback import *
from src.db_models.company import Company
from src.db_models.ipos import *
from src.db_models.news import News
from src.db_models.relationships import *
from src.db_models.events import Event
from src.db_models.INDEX import IndicesTable
from src.db.pgdb_connect import engine


def createTables():
    Base.metadata.create_all(engine)

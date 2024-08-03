from src.db_models.base import Base
from src.db_models.model import User
from src.db_models.feedback import Feedback, Comment
from src.db_models.company import Company
from src.db.pgdb_connect import engine

def createTables():
    Base.metadata.create_all(engine)
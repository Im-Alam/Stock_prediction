from src.db_models.base import Base
from typing import List, Optional
from sqlalchemy import Integer, Enum, ForeignKey, DateTime, func, or_, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse


class Feedback(Base):
    __tablename__ = "web_feedback"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    sentiment : Mapped[int] = mapped_column(Integer, nullable =False)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable = False)
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    #Each feed back related to a user but each user not related to a feedback
    user = relationship("User", back_populates="feedbacks")
    

    def __repr__(self) -> str:
        #In your __repr__ method, using !r ensures that the output includes quotes around strings 
        #and other detailed information about the values,
        return f'Feedback {self.id!r} given by {self.user_id!r}'
    
    @classmethod
    def getFeedback_by_user_id(self, user_id:int):
        session = Session(engine)
        try:
            feedbacks = session.query(Feedback).filter(self.user_id == user_id).all()
            return feedbacks
        except Exception as e:
            session.rollback()
            return apiError(400, 'Failed to fetch user feedback')
        finally:
            session.close()
        



class Comment(Base):
    __tablename__ = 'user_comment'
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    regarding : Mapped[int] = mapped_column(Enum('stock','ipo','index', 'nifty', name='comment_enum'), nullable=True)
    sentiment : Mapped[int] = mapped_column(Integer, nullable = True)
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    user = relationship('User', 
                        back_populates='comments')
    companies = relationship('Company', 
                        secondary='comment_company_association', 
                        back_populates='comments', 
                        passive_deletes=True)


    def __repr__(self) -> str:
        #In your __repr__ method, using !r ensures that the output includes quotes around strings 
        #and other detailed information about the values,
        return f'Comment {self.id!r} posted by {self.user_id!r} with sentiment {self.sentiment!r}'
    
    def get_comment_by_user_id(self, user_id:int):
        #returns list of {comment, date}: [{comment, date},{},{},...]
        pass

    def get_comment_by_company_id(self, company_id):
        #returns list of {comment, date}: [{comment, date},{},{},...]
        pass


from typing import List, Optional
from sqlalchemy import String, Integer, BIGINT, Enum, ForeignKey, DateTime, func, text, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db_models.base import Base
import bcrypt
import os
import jwt
from datetime import datetime, timedelta
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    fullname: Mapped[str] = mapped_column(String(80), nullable=True)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    access_token: Mapped[str] = mapped_column(String, nullable=True)
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    comments = relationship('Comment', back_populates="user", cascade="all, delete-orphan")

    #__init__ method is derived from Base
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.fullname!r})"
    
    #If user want to remove its account
    def removeUser(self, userID):
        session = Session(engine)
        try:
            user = session.query(User).filter_by(id = userID).first()
            session.delete(user)
            session.commit()
        except:
            session.rollback()
            return apiError(500, f"No user exist with id {userID}")
        finally:
            session.close()

    #Find user by id
    @classmethod
    def findUserById(self, userId:int):
        session = Session(engine)
        try:
            #It will return 'None' if no user found. 
            user = session.query(User).filter(User.id == userId).first()
            return user
        except Exception as e:
            session.rollback()
            return apiError(500, f'{e}')
        finally:
            session.close()

    @classmethod
    def findUserByUsename(self, inp_username:str):
        session = Session(engine)
        try:
            #It will return 'None' if no user found. 
            user = session.query(User).filter_by(username = inp_username).first()
            return user
        except Exception as e:
            session.rollback()
            return apiError(500, f'{e}')
        finally:
            session.close()

    @classmethod
    def findUser_OR(self, username_, email_):
        session = Session(engine)
        try:
            user = session.query(User).filter(or_(self.username == username_, self.email == email_)).first()
            return user
        except Exception as e:
            session.rollback()
            return apiError(400, f'Error occured while fething user detail. Error: {e}')
        finally:
            session.close()

    #If user want to update its information
    def updatePassword(self, password):
        session = Session(engine)
        try:
            self.password = password
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, 'Something went wrong while updating password')
        finally:
            session.close()
 
    #Check if password has been modified to update password
    def isPasswordModified(self, password):
        return bool(1 ^ self.isCorrectPassword(password))

    def isCorrectPassword(self, password_:str):
        try:
            return bcrypt.checkpw(password_.encode(), self.password.encode())
        except:
            return apiError(500, 'Saved password is not byte type')
    
    def generateAcessToken(self):
            payload = {
                'user_id': self.id,  # Example user ID
                'username': self.username,
                'fullname': self.fullname,
                'exp': datetime.now() + timedelta(minutes=(int(os.getenv('ACCESS_TOKEN_EXPIRY'))))
            }
            token =  jwt.encode(payload, os.getenv('ACCESS_TOKEN_SECRET'), algorithm='HS256')
            return token

    def generateRefreshToken(self):
        payload ={
                "id" : self.id,
                "exp": datetime.now() + timedelta(days=int(os.getenv('REFRESH_TOKEN_EXPIRY')))
                }
        token = jwt.encode(payload, os.getenv('REFRESH_TOKEN_SECRET'), algorithm = 'HS256')
        return token


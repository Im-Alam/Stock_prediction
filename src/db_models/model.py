from typing import List, Optional
from sqlalchemy import String, Integer, BIGINT, Enum, ForeignKey, DateTime, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import bcrypt
import os
import jwt
from datetime import datetime, timezone
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse


session = Session(engine)

class Base(DeclarativeBase):
    def deselect(self, *arg):
        pass

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


    #__init__ method is derived from Base
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
    #If user want to remove its account
    def removeUser(self, userID):
        try:
            user = session.query(User).filter_by(id =userID).first()
            session.delete(user)
            session.commit()
        except:
            return apiError(500, f"user not exist with id {userID}")

    #During logout we remove acess token and refresh toke from database
    def removeAcessAndRefreshTokens(self):
        pass

    #Find user by id
    def findUserById(self, userId:int):
        #It will return 'None' if no user found. 
        user = session.query(User).filter_by(id = userId).first() 
        return user

    def findUserByUsename(self, inp_username:str):
        #It will return 'None' if no user found. 
        user = session.query(User).filter_by(username = inp_username).first() 
        return user

    #If user want to update its information
    def updateUser(self, ):
        pass

    #Check if password has been modified to update password
    def isPasswordModified(self, password):
        return bool(1 ^ self.isCorrectPassword(password))

    #hash the password before saving or updating
    def hashPassword(self, password):
        try:
            salt = bcrypt.gensalt(rounds=12)
            self.password = bcrypt.hashpw(password, salt)
            return apiResponse(200, 'Password hashed sucessfully')
        except Exception as e:
            return apiError(409, "Error occured while password hashing \n",e)
        
    def isCorrectPassword(self, password):
        return bcrypt.checkpw(password.encode(), self.password)
    
    def generateAcessToken(self):
        return jwt.encode(
            {
                "id" : self.id,
                "username" : self.username,
                "email" : self.email,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=os.getenv('REFRESH_TOKEN_EXPIRY'))
            },
            os.getenv('ACESS_TOKEN_SECRET'),
            algorithm = 'HS256'
        )

    def generrateRefreshToken(self):
        return jwt.encode(
            {
                "id" : self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=os.getenv('REFRESH_TOKEN_EXPIRY'))
            },
            os.getenv('REFRESH_TOKEN_SECRET'),
            algorithm = 'HS256'
        )
        


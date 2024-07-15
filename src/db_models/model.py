from typing import List, Optional
from sqlalchemy import String, Integer, BIGINT, Enum, ForeignKey, DateTime, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import bcrypt
import os
import jwt
from datetime import datetime, timezone
from src.db.pgdb_connect import engine


session = Session(engine)

class Base(DeclarativeBase):
    def deselect(self, *arg):
        self.

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
        pass

    #During logout we remove acess token and refresh toke from database
    def removeAcessAndRefreshTokens(self):
        pass

    #Find user by id
    def findUserById(self, userId:int):
        #It will return 'None' if no user found. 
        user = session.query(User).filter_by(id = userId).first() #first if in case more entries are present
        return user


    #If user want to update its information
    def updateUser(self, ):
        pass

    #Check if password has been modified to update password
    def isPasswordModified(self, password):
        return bool(1 ^ self.isCorrectPassword(password))

    #hash the password before saving or updating
    def hashPassword(self, password):
        salt = bcrypt.gensalt(rounds=12)
        self.password = bcrypt.hashpw(password, salt)

    def isCorrectPassword(self, password):
        return bcrypt.checkpw(password.encode(), self.password)
    
    def generateAcessToken(self):
        return jwt.encode(
            {
                "id" : self.id,
                "username" : self.username,
                "email" : self.email,
                "exp": datetime.datetime.now() + datetime.timedelta(minutes=os.getenv('REFRESH_TOKEN_EXPIRY'))
            },
            os.getenv('ACESS_TOKEN_SECRET'),
            algorithm = 'HS256'
        )

    def generrateRefreshToken(self):
        return jwt.encode(
            {
                "id" : self.id,
                "exp": datetime.datetime.now() + datetime.timedelta(days=os.getenv('REFRESH_TOKEN_EXPIRY'))
            },
            os.getenv('REFRESH_TOKEN_SECRET'),
            algorithm = 'HS256'
        )
        


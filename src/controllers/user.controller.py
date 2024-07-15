from db_models.model import User
from db.pgdb_connect import engine
from sqlalchemy.orm import Session
import jwt
from utils.reqRes import apiError, apiResponse


def generateAccessAndRefreshtoken(userId:int):
    session = Session(engine)
    try:
        user = User.findUserById(userId)
        if(user != None):
            accessToken = user.generateAcessToken()
            refreshToken = user.generateRefreshToken()
            user.access_token = accessToken
            user.refresh_token = refreshToken
            session.commit()
            return (accessToken, refreshToken)
        else:
            print(f"User wit userId {userId} not found!")

    except Exception as e:
        print(e)
        session.rollback()
        return apiError(400, 'Error occured while finding user or token generation')
    finally:
        session.close()


def registerUser(registrationData):
    #get registrationData as object in to function

    check_format_for = {'username', 'password', 'email'}
    #step 1: check if all fields are filled
    missingKeys = check_format_for - registrationData.keys()

    if(len(missingKeys)!=0):
        return apiError(400, 'All fields required')
    
    username, password, email = registrationData.username, registrationData.password, registrationData.email
    
    session = Session(engine)
    try:
        #Now check if user already exist
        user = session.query(User).filter(User.username == username, User.email == email).first()
        if(user):
            return apiError(409, 'User:{username} already exist',format({username}))
        password = bcrypt.
    except Exception as e:
        return apiError(409, f'{e}')
    finally:
        session.close()
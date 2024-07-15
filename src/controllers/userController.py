from db_models.model import User
from db.pgdb_connect import session
from sqlalchemy.orm import Session
import jwt
from utils.reqRes import apiError, apiResponse
from flask import Flask, request, make_response, jsonify
import os


def generateAccessAndRefreshtoken(userId:int):
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


def registerUser(registrationData:dict):

    #get registrationData as object in to function

    check_format_for = {'username', 'password', 'email'}
    #step 1: check if all fields are filled
    missingKeys = check_format_for - registrationData.keys()

    if(len(missingKeys)!=0):
        return apiError(400, 'All fields required')
    
    username_, password_, email_, fullname_ = registrationData.username, registrationData.password, registrationData.email, registrationData.fullname
    try:
        #Now check if user already exist
        user = session.query(User).filter(User.username == username_, User.email == email_).first()
        if(user):
            return apiError(409, 'User:{username_} already exist',format({username_}))
        
        user = User(
            username = username_,
            password = password_,
            fullname = fullname_,
            email = email_
        )
        session.commit()

    except Exception as e:
        return apiError(409, f'{e}')
    finally:
        session.close()


"""
In flask we can make user login by setting token with user id in session
while logout we will pop all the user related data from session


Other way is from cookie

"""
def login():
    username_ = request.form.get('username')
    password_ = request.form.get('password')

    if(not username_ or not password_):
       return apiError(400, 'Both fields required')
    
    user = User.findUserByUsename(username_)

    if(not user):
        return apiError(404, 'User Does not exist')
    
    passwordIsCorrect = user.isCorrectPassword(password_)

    if(not passwordIsCorrect):
        return apiError(401, 'Invalid user credential')
    
    accessToken, refreshToken = generateAccessAndRefreshtoken(user.id)

    userData = user.deselect('password', 'password', 'created_at')

    response = make_response(jsonify(
        status=200,
        user=userData,
        accessToken=accessToken,
        refreshToken=refreshToken,
        message='User logged in successfully'
    ), 200)

    response.set_cookie('accessToken', accessToken, httponly=True, secure=True)
    response.set_cookie('refreshToken', refreshToken, httponly=True, secure=True)
     
    return response



def logout():
    pass


apiResponse.set_cookie()
Response.delete_cookie('cookie_name', 'cookie2_name',httponly=False, ).json({
    "name" : "Imran",
    "email": "imran@jmail.com"
})




def logout():
    accessToken = request.cookies.get('accessToken')
    user = jwt.decode(
        accessToken,
        os.getenv('ACCESS_TOKEN_SECRET' ),
        algorithm='HS256'
    )
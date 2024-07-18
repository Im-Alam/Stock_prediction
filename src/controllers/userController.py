from src.db_models.model import User
from src.db.pgdb_connect import engine
from sqlalchemy.orm import Session
import jwt
from src.utils.reqRes import apiError, apiResponse
from flask import Flask, request, make_response, jsonify, g
import os
from src.utils.hashPW import hashPassword
from src.utils.auth import login_required

def generateAccessAndRefreshtoken(userId:int):
    try:
        session = Session(engine)

        user = User.findUserById(userId)

        if(user != None):
            accessToken = user.generateAcessToken()
            refreshToken = user.generateRefreshToken()

            user.access_token = accessToken
            user.refresh_token = refreshToken

            session.add(user)
            session.commit()
            print('ACCESS token updated')
            return (accessToken, refreshToken)
        else:
            print(f"User with userId {userId} not found!")

    except Exception as e:
        print(e)
        session.rollback()
        return apiError(400, 'Error occured while finding user or token generation')
    finally:
        session.close()


def registerUser():

    username_ = request.form.get('username')
    password_ = request.form.get('password')
    email_ = request.form.get('email')
    fullname_ = request.form.get('fullname')

    if not (username_ and password_ and fullname_ and email_):
        return apiError(400, 'All fields required')
    
    session = Session(engine)

    try:
        #Now check if user already exist
        user = User.findUser_OR(username_, email_)
        if(user):
            return apiError(401, f'username or email already taken')
        
        user = User(
            username = username_,
            password = hashPassword(password_),
            fullname = fullname_,
            email = email_
        )

        session.add(user)
        session.commit()
       
        return apiResponse(200, 'User registered')

    except Exception as e:
        session.rollback()
        return apiError(400, f'{e}')
    finally:
        session.close()


"""
In flask we can make user login by setting token with user id in session
while logout we will pop all the user related data from session

Other way is from cookie

"""

def login():
    try:
        username_ = request.form.get('username')
        password_ = request.form.get('password')
        #print(username_, password_)

        if(not username_ or not password_):
            return apiError(400, 'Both fields required')
    
        user = User.findUserByUsename(username_)
        
        if(not user):
            return apiError(404, 'User Does not exist')
        
        passwordIsCorrect = user.isCorrectPassword(password_)

        if(not passwordIsCorrect):
            return apiError(401, 'Invalid user credential')
        
        accessToken, refreshToken = generateAccessAndRefreshtoken(user.id)

        userData = user.deselect('password', 'password', 'created_at', 'refresh_token')
        
        response = jsonify(
            {
                "status" :200,
                "user":userData,
                "message":f'{username_} logged in successfully'
            })
        response.status_code = 200
        #Other option to set cookie: domain:str, expires:datetime, path:str. 
        response.set_cookie('accessToken', accessToken, httponly=True, secure=False,)
        #response.set_cookie('refreshToken', refreshToken, httponly=True, secure=False)

        return response

    except Exception as e:
        return apiError(500, f'{e}')
     
    

def logout():
    try:
        try:
            token = request.cookies.get('accessToken')
        except:
            token = request.headers.get('accessToken')
        
        if not token:
            return apiError(400, 'User doesn\'t exist') 
        
        try:
            decodedToken = jwt.decode(token, os.getenv('ACCESS_TOKEN_SECRET'), algorithms=['HS256'])
        except Exception as e:
            return apiError(401, f'{e}\nUser session expired or Invalid token')

        user = User.findUserById(decodedToken['user_id'])
        if(not user):
            return apiError(401, 'Invalid access Token')
        
        session = Session(engine)
        try:
            user.access_token = None
            user.refresh_token = None
            print("executing here")
            session.add(user)
            session.commit()
        except:
            session.rollback()
            return apiError(400, 'Error occured while logging out')
        finally:
            session.close()
        
        
        response = jsonify({'message': 'User logged out'})
        response.status_code = 200
        response.delete_cookie('accessToken',httponly=True, secure=False)
        g.user = None  # Clear user data from global context
        
        return response
    except:
        return jsonify({'message': 'No user logged in'}), 400
        


def updatePassword():
    try:
        active_cookie = request.cookies.get('accessToken')

        if not active_cookie:
            return apiError(400, 'User is not logged in')
        
        try:
            decodedCookie = jwt.decode(active_cookie, os.getenv('ACCESS_TOKEN_SECRET'), algorithms=['HS256'])
        except:
            return apiError(400, 'Invalid access token')
        
        
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        
        if not (old_password and new_password):
            return apiError(401, 'Both fields are required')

        user = User.findUserById(decodedCookie['user_id'])

        if not user.isCorrectPassword(old_password):
            return apiError(400,'Old password is incorrect')
        
        user.updatePassword(hashPassword(new_password))

        return apiResponse(200, 'Password updated')

    except Exception as e:
        return apiError(400, f'{e} AND Error occured while updating password')



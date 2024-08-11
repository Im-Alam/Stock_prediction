import jwt
import os
from src.utils.reqRes import apiError;
from src.db_models.user import User
from flask import request, g
from functools import wraps #This used to retain original identity of decorated function

def authorizeUser():
    try:    
        try:
            token = request.cookies.get('accessToken')
        except:
            token = request.headers.get('accessToken')
        
        if not token:
            return apiError(400, 'Invalid user')
        
        try:
            decodedToken = jwt.decode(token, os.getenv('ACCESS_TOKEN_SECRET'), algorithms=['HS256'])
        except Exception as e:
            return apiError(401, f'{e}\nUser session expired or Invalid token')
        

        user = User.findUserById(decodedToken['user_id']).deselect('password', 'refresh_token', 'created_at')

        if(not user):
            return apiError(401, 'Invalid access Token')
        
        #g.user = user

        return 'authorized'

    except Exception as e:
        return apiError(401, f'{e}, Auth failed')

    
#login required dcorator
def login_required(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        response = authorizeUser()
        if response:
            return response
        return func(*arg, **kwargs)
    return wrapper

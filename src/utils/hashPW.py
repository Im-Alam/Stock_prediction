import bcrypt
from src.utils.reqRes import apiError

def hashPassword(password:str):
    try:
        salt = bcrypt.gensalt(rounds=12)
        hasedPassword = bcrypt.hashpw(password.encode(), salt)
        return hasedPassword.decode()
    except Exception as e:
        print(e)
        return apiError(409, "Error occured while password hashing \n")
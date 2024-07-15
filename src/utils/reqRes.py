from flask import Response, Request

#Making subclass of api response
class apiResponse(Response):
    def __init__(self, statusCode:int, message:str):
        self.status = statusCode
        self.message = message
      
class apiError():
    def __init__(self, statusCode, message):
        self.status = statusCode
        self.message = message


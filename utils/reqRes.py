from flask import Response, Request

#Making subclass of api response
class apiResponse(Response):
    def __init__(self, statusCode:int, mimeType:str, ):
        pass



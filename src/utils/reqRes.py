from flask import jsonify

def apiResponse(status, message, data_=None):
    response = jsonify({"status": status, "message": message})
    response.status_code = status
    if data_ != None: 
        response['data'] = data_
    return response

def apiError(status, message):
    response = jsonify({"error": message, "status": status})
    response.status_code = status
    return response
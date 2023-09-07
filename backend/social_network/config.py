def response_error(msg):
    return {
        "status": "Error",
        "msg": msg
    }

def response_success(data):
    return {
        "status": "Success",
        "data": data
    }
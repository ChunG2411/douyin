OAUTH2_INFO = {
    'client_id': 'X9YXvxe73x0T8NkNNBIFbxA4AGFF74uFuaXpYhG4',
    'client_secret': '7UJYfYtVHGCizJwF2HymSqcFH9iEMHU4Yelys1GcuZZzO6FI0MFTfbAgPwJB6umPiTQC2B7rNxYXfy52TfZQ3jg5StO8ME0vJ134CARtQIlL0khTrHvzfaaBhWInBgSa',
}

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
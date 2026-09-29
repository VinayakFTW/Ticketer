def server_response(status_code, message=None, data=None):
    return {
        "data": data,
        "status_code": status_code,
        "message": message,
    }

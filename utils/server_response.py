import json


def server_response(message, status_code, data=None):
    return json.dumps(
        dict(
            data=data,
            status_code=status_code,
            message=message,
        )
    )

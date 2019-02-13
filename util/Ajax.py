def success(message):
    return {
        'code': 200,
        'data': message
    }


def error(message):
    return {
        'code': 500,
        'data': message
    }


def custom(code, message):
    return {
        'code': code,
        'data': message
    }

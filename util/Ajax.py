from flask import jsonify


def success(message):
    return jsonify({
        'code': 200,
        'data': message
    })


def error(message):
    return jsonify({
        'code': 500,
        'data': message
    })


def custom(code, message):
    return jsonify({
        'code': code,
        'data': message
    })

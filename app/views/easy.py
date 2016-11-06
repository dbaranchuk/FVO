from flask import jsonify

def gen_error(message):
    return jsonify(status='error', message=message)

def gen_success(**kwargs):
    return jsonify(status='ok', **kwargs)
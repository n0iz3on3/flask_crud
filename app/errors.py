from flask import jsonify


class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message

    def __repr__(self):
        return f'code\t{self.status_code}\nmessage\t{self.message}'

    def __str__(self):
        return self.__repr__()


def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response

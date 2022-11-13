def json_error(msg, code):
    return {'error': {'code': code, 'message': msg}}, code


class errors:
    not_found = json_error('Not found', 404)
    bad_request = json_error('Invalid request', 400)
    exists = json_error('Forbidden. Already exists', 403)
from apistar import http, Route

from ..database import db


def list_global_tokens() -> dict:
    pass


class ResponseBuilder:

    def __init__(self, *, init_error=False, init_results=False):
        self.response = {}
        
        if init_error:
            self.response['error'] = None
            self.response['results'] = list()

    def set_message(self, message):
        self.response['message'] = message

    def add_result(self, result):
        if 'results' not in self.response:
            self.response['results'] = list()
        self.response['results'].append(result)

    def get_response(self):
        return self.response


def update_global_tokens(tokens: http.RequestData) -> dict:
    response_builder = ResponseBuilder(init_error=True, init_results=True)

    if not tokens:
        response_builder.set_message('Nothing to update.')
        return response_builder.get_response()

    for name, value in tokens.items():
        db.global_tokens.update_one(
            {'name': name},
            {'$set': {'value': value}},
        )
        response_builder.add_result({'name': name, 'value': value})

    response_builder.set_message('Patch applied with success.')
    return response_builder.get_response()


def delete_global_tokens(tokens: http.RequestData):
    print(tokens)


routes = [
    Route('/', method='GET', handler=list_global_tokens),
    Route('/', method='PATCH', handler=update_global_tokens),
    Route('/', method='DELETE', handler=delete_global_tokens),
]

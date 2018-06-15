from apistar.server.components import Component


class ResponseBuilder:

    def __init__(self, *, init_error=False, init_results=False):
        self.response = {}
        
        if init_error:
            self.response['error'] = False
            self.response['results'] = list()

    def set_message(self, message):
        self.response['message'] = message

    def set_error(self, message):
        self.response['message'] = message
        self.response['error'] = True

    def add_result(self, result):
        if 'results' not in self.response:
            self.response['results'] = list()
        self.response['results'].append(result)

    def set_results(self, results):
        self.response['results'] = results

    def get_response(self):
        return self.response


class ResponseBuilderComponent(Component):

    def __init__(self, **kwargs):
        self.init_kwargs = kwargs

    def resolve(self) -> ResponseBuilder:
        return ResponseBuilder(**self.init_kwargs)

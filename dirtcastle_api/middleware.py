from .helpers import create_annotation_agent


class AnnotationAgentMiddleware:

    write_actions = [
        'DELETE',
        'PATCH',
        'POST',
        'PUT',
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.agent = self.create_new_agent()

    def __call__(self, request):
        # inject agent into the request object
        request.annotation_agent = self.agent
        response = self.get_response(request)

        # refresh agent on write actions
        refresh_agent = request.method in self.write_actions
        if getattr(response, 'refresh_agent', refresh_agent):
            self.agent = self.create_new_agent()

        return response

    def create_new_agent(self):
        return create_annotation_agent()

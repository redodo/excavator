import falcon

from .something import something


class ThingsResource:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {'message': 'Hello, World!2'}


app = falcon.API()
app.add_route('/things', ThingsResource())

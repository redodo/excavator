import falcon

from .database import db


class TokenCollection:

    def on_get(self, req, resp):
        """Lists all tokens"""
        resp.media = {
            token['name']: token['value']
            for token in db.tokens.find()
        }

    def on_put(self, req, resp, name):
        pass


class TokenItem:
    pass


app = falcon.API()
app.add_route('/tokens', TokenCollection())
app.add_route('/tokens/{name}', TokenItem())


def run_server(host, port, **options):
    from werkzeug.serving import run_simple
    run_simple(host, port, app, **options)

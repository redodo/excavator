import falcon
import pymongo

from .database import db


class MongoMediaComponent:

    PYMONGO_RESULT_CLASSES = (
        pymongo.results.DeleteResult,
        pymongo.results.InsertOneResult,
        pymongo.results.UpdateResult,
    )

    def process_response(self, req, resp, resource, req_succeeded):
        if not hasattr(resp, 'mongo'):
            return

        if resp.mongo is None:
            raise falcon.HTTPNotFound(
                description='helloworld'
            )
        elif isinstance(resp.mongo, pymongo.cursor.Cursor):
            results = list(resp.mongo)
            for result in results:
                result.pop('_id')
            resp.media = results
        elif isinstance(resp.mongo, dict):
            resp.mongo.pop('_id')
            resp.media = resp.mongo
        elif isinstance(resp.mongo, self.PYMONGO_RESULT_CLASSES):
            pass
        else:
            raise NotImplementedError(
                'resp.mongo is of unknown type %s'
                % type(resp.mongo)
            )
 

class TokenCollection:

    def on_get(self, req, resp):
        """Lists all tokens"""
        resp.mongo = db.tokens.find()


class TokenItem:

    def on_get(self, req, resp, name):
        resp.mongo = db.tokens.delete_one({'name': name})
        # resp.mongo = db.tokens.find_one({'name': name})

    def on_put(self, req, resp, name):
        value = req.media.get('pattern')
        resp.mongo = db.tokens.insert_one({'name': name, 'pattern': value})

    def on_delete(self, req, resp, name):
        resp.mongo = db.tokens.delete_one({'name': name})


app = falcon.API(middleware=[MongoMediaComponent()])
app.add_route('/tokens', TokenCollection())
app.add_route('/tokens/{name}', TokenItem())


def run_server(host, port, **options):
    from werkzeug.serving import run_simple
    run_simple(host, port, app, **options)

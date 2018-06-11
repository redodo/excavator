import typing

import click
import pymongo
from apistar import App, Route, types, validators, http
from apistar.server.components import Component

from .database import db


def response(value):

    if isinstance(value, pymongo.cursor.Cursor):
        results = [dict(r) for r in value]
        for r in results:
            del r['_id']
        return results

    raise NotImplementedError(
        'a response could not be created for type %s'
        % type(value)
    )


class Annotator(types.Type):
    name = validators.String()
    case_sensitive = validators.Boolean(default=False)


def list_annotators() -> typing.List[Annotator]:
    return response(db.annotators.find())


def get_annotator(name: str):
    """Returns the settings, tokens, and patterns of an annotator.

    TODO: add dedicated endpoints to retrieve just tokens, patterns, or settings
    """
    return response(db.annotators.find_one({'name': name}))


def create_annotator(annotator: Annotator):
    result = db.annotators.insert_one(dict(annotator))


def update_annotator(name: str, annotator: Annotator):
    # FIXME: All annotator attributes with defaults will be reset when not sent. The annotator object passed to this function shouldn't set these default attributes, or mark them as such. In this function we actually do not care about unset attributes. It is just for updating the ones that are set.
    result = db.annotators.update_one({'name': name}, {'$set': dict(annotator)})


def delete_annotator(name: str):
    """Deletes something"""
    result = db.annotators.delete_one({'name': name})


def get_global_tokens() -> dict:
    result = db.globals.find_one({'key': 'tokens'})
    print(result)
    return result['values'] or {}


def set_global_tokens(tokens: http.RequestData):
    values = db.globals.find_one({'key': 'tokens'})['values']
    values.update(dict(tokens))
    # FIXME: Right now, the entire set of tokens are reset on each single update. This should be optimized to let MongoDB apply the diff of the update, and not do an entire replace.
    result = db.globals.update_one({'key': 'tokens'}, {'$set': {'values': values}})
    print(result)


def delete_global_token(name: str):
    values = db.globals.find_one({'key': 'tokens'})['values']
    del values[name]
    # FIXME: See fixme in set_global_tokens
    result = db.globals.update_one({'key': 'tokens'}, {'$set': {'values': values}})
    print(result)



routes = [
    Route('/tokens', method='GET', handler=get_global_tokens),
    Route('/tokens', method='PATCH', handler=set_global_tokens),
    Route('/tokens/{name}', method='DELETE', handler=delete_global_token),
    Route('/annotators', method='GET', handler=list_annotators),
    Route('/annotators', method='POST', handler=create_annotator),
    Route('/annotators/{name}', method='GET', handler=get_annotator),
    Route('/annotators/{name}', method='PATCH', handler=update_annotator),
    Route('/annotators/{name}', method='DELETE', handler=delete_annotator),
]
app = App(routes=routes)

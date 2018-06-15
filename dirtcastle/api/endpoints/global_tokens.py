from apistar import http, Route, types, validators

from ..database import db
from ..response import ResponseBuilder


class Token(types.Type):
    name = validators.String(min_length=1)
    value = validators.String(min_length=1)


def list_global_tokens(r: ResponseBuilder) -> dict:
    r.set_results({
        token['name']: token['value']
        for token in db.global_tokens.find()
    })
    return r.get_response()


def update_global_tokens(tokens: http.RequestData, r: ResponseBuilder) -> dict:
    """Updates multiple global tokens."""
    if not tokens:
        r.set_message('Nothing to update.')
        return r.get_response()

    for name, value in tokens.items():
        db.global_tokens.update_one(
            {'name': name},
            {'$set': {'value': value}},
            upsert=True,
        )
        r.add_result({'name': name, 'value': value})

    r.set_message('Patch applied with success.')
    return r.get_response()


def replace_global_tokens(tokens: http.RequestData, r: ResponseBuilder) -> dict:
    """Replaces the set of global tokens with the given set."""
    if not tokens:
        r.set_error('No tokens provided. Deletion of tokens prevented')
        return r.get_response()

    db.global_tokens.delete_many({})
    for name, value in tokens.items():
        db.global_tokens.insert_one({'name': name, 'value': value})

    r.set_results(tokens)
    return r.get_response()


def delete_global_tokens(tokens: http.RequestData):
    """TODO: Deletes all the given global tokens."""


def delete_global_token(name: str, r: ResponseBuilder):
    """Deletes a single global token."""
    db.global_tokens.delete_one({'name': name})
    return r.get_response()


routes = [
    Route('/', method='GET', handler=list_global_tokens),
    Route('/', method='POST', handler=replace_global_tokens),
    Route('/', method='PATCH', handler=update_global_tokens),
    Route('/', method='DELETE', handler=delete_global_tokens),
    Route('/{name}', method='DELETE', handler=delete_global_token),
]

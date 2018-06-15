from apistar import Route, types, validators

from ..response import ResponseBuilder


class Something(types.Type):
    name = validators.String(min_length=1)
    case_sensitive = validators.Boolean(allow_null=True, default=False)


def test_something(something: Something):
    return something


routes = [
    Route('/', method='PATCH', handler=test_something),
]

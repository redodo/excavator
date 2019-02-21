def default_json_serialize(obj):
    """TODO: RENAME?"""
    # allow objects, such as annotations, to be serializeable
    return obj.__dict__

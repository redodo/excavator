import json


class DictSerializer:

    def to_dict(self):
        raise NotImplementedError(
            '%s does not implement `to_dict`'
            % self.__class__.__name__
        )

    @classmethod
    def from_dict(cls, d):
        raise NotImplementedError(
            '%s does not implement `from_dict`'
            % cls.__name__
        )


class DictJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            return super().default(obj)


class JsonSerializer(DictSerializer):

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), cls=DictJsonEncoder, **kwargs)

    @classmethod
    def from_json(cls, d):
        return cls.from_dict(json.loads(d))

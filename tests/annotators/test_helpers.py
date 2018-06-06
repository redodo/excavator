import json

from dirtcastle.annotations.base import Annotation
from dirtcastle.annotators import registry
from dirtcastle.annotators.helpers import (
    build_annotator,
    build_annotator_from_dict,
)


def test_build_annotator():
    annotator_class = build_annotator(
        base='text',
        type_name='Hello',
        tokens={'x': 'hello'},
        patterns=['{x}'],
    )
    assert annotator_class in registry
    annotator = annotator_class()

    text = 'hello world'
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='Hello'),
    ]


def test_build_annotator_from_dict():
    raw_json = '''
    {
        "base": "text",
        "type": "World",
        "tokens": {"x": "world"},
        "patterns": ["{x}"]
    }
    '''
    annotator_data = json.loads(raw_json)

    annotator_class = build_annotator_from_dict(annotator_data)
    assert annotator_class in registry
    annotator = annotator_class()

    text = 'hello world'
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('world', (6, 11), type='World'),
    ]

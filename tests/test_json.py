import json

from unearth.annotations.text import AnnotatedText
from unearth.annotators.agent import Agent
from unearth.annotators.base import Annotator
from unearth.utils.serialize import default_json_serialize


def test_json_integrity():
    text = '''
    hello
    world
    '''

    agent = Agent()
    agent.create_annotator(
        'HelloWorld',
        patterns=('hello', 'world'),
    )

    annotated_text = agent.annotate(text)
    annotated_text_json = json.dumps(
        annotated_text,
        default=default_json_serialize,
    )
    # Although it's not supported to recreate objects from json,
    # we parse the data from json to check the integrity.
    data = json.loads(annotated_text_json)
    assert data['lines'][1]['annotations'][0] == {
        'text': 'hello',
        'span': [0, 5],
        'type': 'HelloWorld',
        'score': 1.0,
        'data': None,
    }
    assert data['lines'][2]['annotations'][0] == {
        'text': 'world',
        'span': [0, 5],
        'type': 'HelloWorld',
        'score': 1.0,
        'data': None,
    }

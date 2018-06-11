from dirtcastle.annotations.text import AnnotatedText
from dirtcastle.annotators.agent import Agent
from dirtcastle.annotators.base import Annotator


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
    annotated_text_json = annotated_text.to_json(indent=4)
    recreated_annotated_text = AnnotatedText.from_json(annotated_text_json)

    assert annotated_text == recreated_annotated_text

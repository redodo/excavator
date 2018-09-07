from unearth.annotations.base import Annotation
from unearth.annotators.agent import Agent
from unearth.annotators.base import Annotator


def test_agent():
    text = '''
        hello
        world
    '''

    agent = Agent()
    agent.add_annotator(
        Annotator(
            'HelloWorld',
            patterns=('hello', 'world'),
        )
    )
    annotated_text = agent.annotate(text)

    assert len(annotated_text.lines) == 4
    assert annotated_text.lines[1].cells[0][0] == \
        Annotation('hello', (0, 5), type='HelloWorld')
    assert annotated_text.lines[2].cells[0][0] == \
        Annotation('world', (0, 5), type='HelloWorld')


def test_agent_create_annotator():
    text = 'hello world'

    agent = Agent()
    agent.create_annotator(
        'Hello',
        patterns='hello',
    )
    annotated_text = agent.annotate(text)

    assert annotated_text.lines[0].annotations == [
        Annotation('hello', (0, 5), type='Hello'),
    ]

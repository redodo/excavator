from dirtcastle.annotations.base import Annotation
from dirtcastle.annotators.agent import Agent
from dirtcastle.annotators.base import TextAnnotator
from dirtcastle.annotators.helpers import annotate


def test_agent():
    text = '''
        hello
        world
    '''

    class HelloWorldAnnotator(TextAnnotator):
        patterns = ('hello', 'world')

    agent = Agent()
    annotated_text = agent.annotate(text)

    assert len(annotated_text.lines) == 4
    assert annotated_text.lines[1].cells[0][0] == \
        Annotation('hello', (0, 5), type='HelloWorld')
    assert annotated_text.lines[2].cells[0][0] == \
        Annotation('world', (0, 5), type='HelloWorld')


def test_annotate_helper():
    text = '''
        hello
        world
    '''

    class HelloWorldAnnotator(TextAnnotator):
        patterns = ('hello', 'world')

    agent = Agent()
    a = agent.annotate(text)
    b = annotate(text)

    assert a == b

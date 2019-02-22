from excavator.annotators.agent import Agent
from excavator.annotators.base import Annotator
from excavator.strategies.density import IncreaseDensityStrategy


def test_increase_density():
    agent = Agent()
    agent.add_strategy(IncreaseDensityStrategy(10))
    agent.add_annotator(
        Annotator(
            'Greeting',
            patterns=('hello', 'hi', 'greetings'),
        )
    )

    text = '''
    hello
    hi
    hello

    hello
    greetings
    greetings
    '''

    annotated_text = agent.annotate(text)

    assert annotated_text.lines[0].text == ''
    assert annotated_text.lines[1].text == 'hello hi hello'
    assert annotated_text.lines[2].text == 'hello greetings greetings'


def test_empty():
    agent = Agent()
    agent.add_strategy(IncreaseDensityStrategy(10))
    annotated_text = agent.annotate('')

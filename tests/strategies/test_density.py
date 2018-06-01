from dirtcastle.annotators.agent import Agent
from dirtcastle.annotators.base import TextAnnotator
from dirtcastle.strategies.density import IncreaseDensityStrategy


def test_increase_density():
    agent = Agent()

    agent.add_strategy(
        IncreaseDensityStrategy(12)
    )

    class GreetingAnnotator(TextAnnotator):
        patterns = ('hello', 'hi', 'greetings')

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

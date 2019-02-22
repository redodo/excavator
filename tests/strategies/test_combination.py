from excavator.annotators.agent import Agent
from excavator.strategies.combination import CombinationStrategy


def test_combination_strategy():
    agent = Agent()
    agent.add_strategy(CombinationStrategy({
        ('Hello', 'World'): 2.0,
    }))
    agent.create_annotator('Hello', patterns='hello')
    agent.create_annotator('Greeting', patterns='hello')
    agent.create_annotator('World', patterns='world')

    text = 'hello world'

    annotated_text = agent.annotate(text)
    annotated_text.disambiguate(discard_others=True)
    
    assert annotated_text.lines[0].annotations[0].type == 'Hello'
    assert annotated_text.lines[0].annotations[1].type == 'World'
    assert annotated_text.lines[0].annotations[0].score == 2.0
    assert annotated_text.lines[0].annotations[1].score == 2.0

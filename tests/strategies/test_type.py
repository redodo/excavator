from dirtcastle.annotations.base import Annotation
from dirtcastle.annotators.agent import Agent
from dirtcastle.annotators.base import TextAnnotator
from dirtcastle.strategies.type import NearbyTypeStrategy


def test_nearby_type():
    agent = Agent()

    agent.add_strategy(
        NearbyTypeStrategy(
            # similar types in cells directly above or below get
            # a factor 2.0 boost
            max_boost=2.0,
            min_boost=1.0,
            v_reach=1,
            h_reach=0,
        )
    )

    class TimeAnnotator(TextAnnotator):
        patterns = [str(h) for h in range(1, 25)]

    class ContainerAnnotator(TextAnnotator):
        patterns = ('20', '40ft')

    text = '''
    container  hour
    20         13
    40ft       15
    20         20
    '''

    annotated_text = agent.annotate(text)
    annotated_text.disambiguate(discard_others=True)

    # the disambiguator should have enough information to figure out
    # that the left column consists of containers
    assert annotated_text.lines[2].annotations[0].type == 'Container'
    assert annotated_text.lines[2].annotations[1].type == 'Time'

    assert annotated_text.lines[3].annotations[0].type == 'Container'
    assert annotated_text.lines[3].annotations[1].type == 'Time'

    assert annotated_text.lines[4].annotations[0].type == 'Container'
    assert annotated_text.lines[4].annotations[1].type == 'Time'

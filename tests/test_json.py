from dirtcastle.annotations.text import AnnotatedText
from dirtcastle.annotators.base import TextAnnotator
from dirtcastle.annotators.helpers import annotate


def test_json_integrity():
    text = '''
    hello
    world
    '''

    class HelloWorldAnnotator(TextAnnotator):
        patterns = ('hello', 'world')

    annotated_text = annotate(text)
    annotated_text_json = annotated_text.to_json(indent=4)
    print(annotated_text_json)
    recreated_annotated_text = AnnotatedText.from_json(annotated_text_json)

    assert annotated_text == recreated_annotated_text

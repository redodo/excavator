from .agent import default_agent
from .base import TextAnnotator, RegexAnnotator


base_annotators = {
    'text': TextAnnotator,
    'regex': RegexAnnotator,
}


def build_annotator(base, type_name, patterns, case_sensitive=None):
    base_class = base_annotators[base]
    class_name = '%sAnnotator' % type_name

    annotator_class = type(
        class_name,
        (base_class,),
        {
            'patterns': patterns,
            'case_sensitive': case_sensitive,
        },
    )

    return annotator_class


def build_annotator_from_dict(data):
    data['type_name'] = data.pop('type', data.get('type_name', None))
    return build_annotator(**data)


def annotate(*args, **kwargs):
    return default_agent.annotate(*args, **kwargs)

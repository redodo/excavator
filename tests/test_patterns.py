from dirtcastle.patterns.builder import RegexBuilder


def test_builder():
    tokens = {
        'greetings': '/(hello|hi)/',
        'object': '/(world|there)/',
        '??': '?',
        '?': '/?/',
        'comma': ',',
        'sep': '/{comma}{?} /',
    }
    patterns = [
        '{greetings}{sep}{object}{??}{?}'
    ]

    builder = RegexBuilder(tokens, patterns)
    regexes = builder.compile_all()
    regex = regexes[0]

    assert regex.match('hello world')
    assert regex.match('hi, there')
    assert not regex.match('hello,? world')
    assert regex.match('hi world?')
    assert regex.match('hello, world?')
    assert not regex.match('hello, there?')

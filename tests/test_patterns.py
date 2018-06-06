from dirtcastle.patterns.builder import PatternBuilder


def test_builder():
    raw_tokens = {
        'greetings': '/(hello|hi)/',
        'object': '/(world|there)/',
        '??': '?',
        '?': '/?/',
        'comma': ',',
        'dot': '.',
        'sep': '/({comma}|{dot}){?} /',
    }
    raw_pattern = '{greetings}{sep}{object}{??}{?}'

    builder = PatternBuilder(raw_tokens)
    pattern = builder.compile(raw_pattern)

    assert pattern.match('hello world')
    assert pattern.match('hi, there')
    assert not pattern.match('hello,? world')
    assert pattern.match('hi world?')
    assert pattern.match('hello, world?')
    assert pattern.match('hi. world')

def find_all(sub, text, case_sensitive=False):
    source = text
    if not case_sensitive:
        sub = sub.lower()
        text = text.lower()

    sublen = len(sub)
    index = -1
    while True:
        index = text.find(sub, index + 1)
        if index == -1:
            break
        span = slice(index, index + sublen)
        yield source[span], span

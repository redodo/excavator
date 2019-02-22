def kwargs_notation(d):
    return '(%s)' % ', '.join(['%s=%s' % (k, repr(v)) for k, v in d.items()])

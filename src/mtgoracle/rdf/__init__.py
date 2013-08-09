from urllib import quote
from string import maketrans


def quote_name(name):
    replacements = [(' ', '_'),
                    (u'\u201c', u'"'),
                    (u'\u201d', u'"')]
    name = str(name)
    for old, new in replacements:
        name = name.replace(old, new)
    return quote(name)

from urllib import quote
from string import maketrans


def quote_name(name):
    replacements = [(u' ', u'_'),
                    (u'\u201c', u'"'),
                    (u'\u201d', u'"')]
    name = unicode(name)
    for old, new in replacements:
        name = name.replace(old, new)
    return quote(name)

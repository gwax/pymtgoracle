from os.path import expanduser, join, split
from sqlalchemy import create_engine


dbPath = '~/mtgoracle.sqlite'
dbPath = expanduser(join(*split(dbPath)))


def get_engine(path=dbPath, echo=False):
    return create_engine('sqlite:///%s' % path, echo=echo)

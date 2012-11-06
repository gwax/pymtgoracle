from sqlalchemy import create_engine
from os.path import expanduser, join, split


dbPath = '~/mtgoracle.sqlite'
dbPath = expanduser(join(*split(dbPath)))


def get_engine(path=dbPath, echo=False):
    return create_engine('sqlite:///%s' % path, echo=echo)

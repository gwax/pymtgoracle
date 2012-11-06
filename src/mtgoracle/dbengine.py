from sqlalchemy import create_engine


dbPath = 'mtgoracle.sqlite'
engine = create_engine('sqlite:///%s' % dbPath, echo=True)
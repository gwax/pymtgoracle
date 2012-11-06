from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


maker = sessionmaker(autoflush=True, autocommit=False)
DBSession = scoped_session(maker)


DeclarativeBase = declarative_base()


metadata = DeclarativeBase.metadata


def init_model(engine):
    metadata.create_all(bind=engine)
    DBSession.configure(bind=engine)


from mtgoracle.model.card import Card
from mtgoracle.model.cardset import CardSet

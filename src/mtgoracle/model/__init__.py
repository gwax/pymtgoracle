from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


maker = sessionmaker(autoflush=True, autocommit=False)
DBSession = scoped_session(maker)


DeclarativeBase = declarative_base()


metadata = DeclarativeBase.metadata


def init_model(engine):
    DBSession.configure(bind=engine)

from mtgoracle.model.card import Card
from mtgoracle.model.cardprinting import CardPrinting
from mtgoracle.model.cardset import CardSet
from mtgoracle.model.cardtypes import CardType, CardSubtype

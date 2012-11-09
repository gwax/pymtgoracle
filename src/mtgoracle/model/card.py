from sqlalchemy import Column, Unicode, PickleType, Integer
from mtgoracle.model import DeclarativeBase


class Card(DeclarativeBase):
    __tablename__ = 'mtgoracle_cards'
    name = Column(Unicode(255), primary_key=True, unique=True, nullable=False)
    cmc = Column(Integer)
    cost = Column(Unicode(31))
    types = Column(PickleType)
    subtypes = Column(PickleType)
    rules = Column(PickleType)
    power = Column(Unicode(5))
    toughness = Column(Unicode(5))

    # {Special methods
    def __repr__(self):
        return ('<Card: %s>' % self.name).encode('utf-8')

    def __unicode__(self):
        return unicode(self.name)

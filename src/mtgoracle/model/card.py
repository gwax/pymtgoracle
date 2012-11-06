from sqlalchemy import Column, Unicode, PickleType
from sqlalchemy.ext.associationproxy import association_proxy
from mtgoracle.model import DeclarativeBase


class Card(DeclarativeBase):
    __tablename__ = 'mtgoracle_cards'
    name = Column(Unicode(255), primary_key=True, unique=True, nullable=False)
    editions = association_proxy('setlistings', 'set')

    link = Column(Unicode(255))
    artist = Column(Unicode(255))
    cost = Column(Unicode(255))

    supertypes = Column(PickleType)
    subtypes = Column(PickleType)
    power = Column(Unicode(255))
    toughness = Column(Unicode(255))

    rarity = Column(Unicode(255))
    edition = Column(Unicode(255))
    text = Column(Unicode(255))
    flavor_text = Column(Unicode(255))
    legalities = Column(Unicode(255))
    rulings = Column(Unicode(255))
    image = Column(Unicode(255))
    otherpart = Column(Unicode(255))

    # {Special methods
    def __repr__(self):
        return ('<Card: %s>' % self.name).encode('utf-8')

    def __unicode__(self):
        return unicode(self.name)

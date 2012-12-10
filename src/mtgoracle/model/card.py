from mtgoracle.model import DeclarativeBase, DBSession
from mtgoracle.model.cardtypes import CardSubtype, CardType
from sqlalchemy import Column, Unicode, Integer, Text, Boolean
from sqlalchemy.orm import relationship


class Card(DeclarativeBase):
    __tablename__ = 'mtgoracle_cards'
    name = Column(Unicode(127), primary_key=True, unique=True, nullable=False)
    cmc = Column(Integer)
    cost = Column(Unicode(31))
    rules = Column(Text(convert_unicode=True))
    power = Column(Unicode(5))
    toughness = Column(Unicode(5))
    loyalty = Column(Integer)
    legendary = Column(Boolean, default=False)

    types = relationship('CardType', secondary='mtgoracle_card_types')
    subtypes = relationship('CardSubtype', secondary='mtgoracle_card_subtypes')

    # { Special methods
    def __repr__(self):
        return ('<Card: %s>' % self.name).encode('utf-8')

    def __unicode__(self):
        return unicode(self.name)

    # { Search options
    @staticmethod
    def by_name(namestr):
        return DBSession.query(Card).filter_by(name=namestr).first()

    @staticmethod
    def with_type(typestr):
        return DBSession.query(Card).\
                filter(Card.types.any(CardType.name == typestr)).all()

    @staticmethod
    def with_subtype(stypestr):
        return DBSession.query(Card).\
                filter(Card.subtypes.any(CardSubtype.name == stypestr)).all()

from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import types
from pymtgoracle.model import base
from pymtgoracle.model import cardtypes


class Card(base.Base):
    __tablename__ = 'mtgoracle_cards'
    name = schema.Column(
        types.Unicode(127), primary_key=True, unique=True, nullable=False)
    cmc = schema.Column(types.Integer)
    cost = schema.Column(types.Unicode(31))
    colorid = schema.Column(types.Unicode(1))
    rules = schema.Column(types.UnicodeText)
    power = schema.Column(types.Unicode(5))
    toughness = schema.Column(types.Unicode(5))
    loyalty = schema.Column(types.Integer)

    types = orm.relationship('CardType', secondary='mtgoracle_card_types')
    subtypes = orm.relationship('CardSubtype',
                                secondary='mtgoracle_card_subtypes')

    # { Special methods
    def __repr__(self):
        return '<Card: %s>' % self.name

    def __str__(self):
        return self.name

    # { Search options
    @classmethod
    def by_name(cls, session, cardname):
      return session.query(cls).filter_by(name=cardname).first()

    @classmethod
    def with_type(cls, session, typename):
      return session.query(cls).filter(
          Card.types.any(cardtypes.CardType.name == typename)).all()

    @classmethod
    def with_subtype(cls, session, stypename):
      return session.query(cls).filter(
          Card.subtypes.any(cardtypes.CardSubtype.name == stypename)).all()

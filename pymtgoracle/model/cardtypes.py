from sqlalchemy import schema
from sqlalchemy import types

from pymtgoracle.model import base


card_type_association = schema.Table(
    'mtgoracle_card_types', base.Base.metadata,
    schema.Column('cardname', types.Unicode(127),
                  schema.ForeignKey('mtgoracle_cards.name')),
    schema.Column('type', types.Unicode(15),
                  schema.ForeignKey('mtgoracle_types.name')))

card_subtype_association = schema.Table(
    'mtgoracle_card_subtypes', base.Base.metadata,
    schema.Column('cardname', types.Unicode(127),
                  schema.ForeignKey('mtgoracle_cards.name')),
    schema.Column('type', types.Unicode(15),
                  schema.ForeignKey('mtgoracle_subtypes.name')))


class CardType(base.Base):
  __tablename__ = 'mtgoracle_types'
  name = schema.Column(types.Unicode(15), primary_key=True,
                       unique=True, nullable=False)

  # {Special methods
  def __repr__(self):
    return '<CardType: %s>' % self.name

  def __str__(self):
    return self.name


class CardSubtype(base.Base):
  __tablename__ = 'mtgoracle_subtypes'
  name = schema.Column(types.Unicode(15), primary_key=True,
                       unique=True, nullable=False)

  # {Special methods
  def __repr__(self):
    return '<SubType: %s>' % self.name

  def __str__(self):
    return self.name

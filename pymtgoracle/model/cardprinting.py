from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy.ext import hybrid
from sqlalchemy.orm import collections

from pymtgoracle.model import base


class CardPrinting(base.Base):
  __tablename__ = 'mtgoracle_setlists'
  setcode = schema.Column(
      types.Unicode(15), schema.ForeignKey(
          'mtgoracle_sets.code', onupdate='CASCADE', ondelete='CASCADE'),
      primary_key=True)
  cardname = schema.Column(
      types.Unicode(255), schema.ForeignKey(
          'mtgoracle_cards.name', onupdate='CASCADE', ondelete='CASCADE'),
      primary_key=True)
  number = schema.Column(types.Integer, primary_key=True)
  variant = schema.Column(types.Integer, primary_key=True, default=0)

  rarity = schema.Column(types.Unicode(15))
  link = schema.Column(types.Unicode(255))
  imagelink = schema.Column(types.Unicode(255))
  artist = schema.Column(types.Unicode(255))
  flavor = schema.Column(types.UnicodeText)

  card = orm.relationship('Card', backref='printings')
  set = orm.relationship(
      'CardSet', backref=orm.backref('printlist',
      collection_class=collections.attribute_mapped_collection('setid')))

  # {Special methods
  def __repr__(self):
    
    return '<CardPrinting: %s-%s: %s' % (
        self.setcode, repr(self.setid), self.cardname)

  def __str__(self):
      return '%s: %s' % (self.setcode, self.cardname)

  # {Properties
  @hybrid.hybrid_property
  def setid(self):
    return (self.number, self.variant)

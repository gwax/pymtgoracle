from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy.ext import associationproxy

from pymtgoracle.model import base


class CardSet(base.Base):
  __tablename__ = 'mtgoracle_sets'
  code = schema.Column(
      types.Unicode(15), primary_key=True, unique=True, nullable=False)
  name = schema.Column(types.Unicode(255), unique=True, nullable=False)
  block = schema.Column(types.Unicode(255))
  link = schema.Column(types.Unicode(255))
  release_date = schema.Column(types.DateTime)

  cards = associationproxy.association_proxy('printlist', 'card')

  # {Special Methods
  def __repr__(self):
    return '<CardSet: %s - %s>' % (self.code.upper(), self.name)

  def __str__(self):
      return self.code

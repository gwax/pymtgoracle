from sqlalchemy import Column, Unicode
from mtgoracle.model import DeclarativeBase


class Card(DeclarativeBase):
    __tablename__ = 'mtgoracle_cards'
    name = Column(Unicode(255), primary_key=True, unique=True, nullable=False)

    # {Special methods
    def __repr__(self):
        return ('<Card: %s>' % self.name).encode('utf-8')

    def __unicode__(self):
        return unicode(self.name)

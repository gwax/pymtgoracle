from sqlalchemy import Column, Unicode, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from mtgoracle.model import DeclarativeBase


class SetLists(DeclarativeBase):
    __tablename__ = 'mtgoracle_setlists'
    setcode = Column(Unicode(15), ForeignKey('mtgoracle_sets.code',
                     onupdate='CASCADE', ondelete='CASCADE'),
                     primary_key=True)
    cardname = Column(Unicode(255), ForeignKey('mtgoracle_cards.name',
                      onupdate='CASCADE', ondelete='CASCADE'),
                      primary_key=True)
    number = Column(Integer)

    card = relationship('Card', backref='setlistings')
    set = relationship('CardSet', backref=backref('setlist',
                    collection_class=attribute_mapped_collection('number')))


class CardSet(DeclarativeBase):
    __tablename__ = 'mtgoracle_sets'
    code = Column(Unicode(15),
                  primary_key=True, unique=True, nullable=False)
    name = Column(Unicode(255), unique=True, nullable=False)
    block = Column(Unicode(255))
    link = Column(Unicode(255))
    release_date = Column(DateTime)

    cards = association_proxy('setlist', 'card',
                      creator=lambda k, v: SetLists(number=k, card=v))

    # {Special Methods
    def __repr__(self):
        return ('<CardSet: %s: %s>' % (self.code, self.name)).encode('utf-8')

    def __unicode__(self):
        return unicode(self.code)

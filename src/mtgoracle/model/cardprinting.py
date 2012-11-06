from sqlalchemy import Column, Unicode, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from mtgoracle.model import DeclarativeBase


class CardPrinting(DeclarativeBase):
    __tablename__ = 'mtgoracle_setlists'
    setcode = Column(Unicode(15), ForeignKey('mtgoracle_sets.code',
                     onupdate='CASCADE', ondelete='CASCADE'),
                     primary_key=True)
    cardname = Column(Unicode(255), ForeignKey('mtgoracle_cards.name',
                      onupdate='CASCADE', ondelete='CASCADE'),
                      primary_key=True)
    setnumber = Column(Integer, primary_key=True)
    variant = Column(Integer, primary_key=True)

    link = Column(Unicode(255))
    artist = Column(Unicode(255))

    card = relationship('Card', backref='printings')
    set = relationship('CardSet', backref=backref('printlist',
                    collection_class=attribute_mapped_collection('setnumber')))

    # {Special methods
    def __repr__(self):
        return ('<CardPrinting: %s-%d: %s>' %
                (self.setcode, self.setnumber, self.cardname)).encode('utf-8')

    def __unicode__(self):
        return unicode(self.name)
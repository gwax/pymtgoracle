from mtgoracle.model import DeclarativeBase
from sqlalchemy import Column, Unicode, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection


class CardPrinting(DeclarativeBase):
    __tablename__ = 'mtgoracle_setlists'
    setcode = Column(Unicode(15), ForeignKey('mtgoracle_sets.code',
                     onupdate='CASCADE', ondelete='CASCADE'),
                     primary_key=True)
    cardname = Column(Unicode(255), ForeignKey('mtgoracle_cards.name',
                      onupdate='CASCADE', ondelete='CASCADE'),
                      primary_key=True)
    number = Column(Integer, primary_key=True)
    variant = Column(Integer, primary_key=True)

    rarity = Column(Unicode(15))
    link = Column(Unicode(255))
    artist = Column(Unicode(255))
    flavor = Column(Unicode(255))

    card = relationship('Card', backref='printings')
    set = relationship('CardSet', backref=backref('printlist',
                    collection_class=attribute_mapped_collection('setnumber')))

    # {Special methods
    def __repr__(self):
        return ('<CardPrinting: %s-%d%s: %s>' %
                (self.setcode,
                 self.number,
                 '.' + str(self.variant) if self.variant > 0 else '',
                 self.cardname)).encode('utf-8')

    def __unicode__(self):
        return unicode(self.name)

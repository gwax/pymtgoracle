from mtgoracle.model import DeclarativeBase
from mtgoracle.model.cardprinting import CardPrinting
from sqlalchemy import Column, Unicode, DateTime
from sqlalchemy.ext.associationproxy import association_proxy


class CardSet(DeclarativeBase):
    __tablename__ = 'mtgoracle_sets'
    code = Column(Unicode(15),
                  primary_key=True, unique=True, nullable=False)
    name = Column(Unicode(255), unique=True, nullable=False)
    block = Column(Unicode(255))
    link = Column(Unicode(255))
    release_date = Column(DateTime)

    cards = association_proxy('printlist', 'card',
                      creator=lambda k, v: CardPrinting(setnumber=k, card=v))

    # {Special Methods
    def __repr__(self):
        return ('<CardSet: %s - %s>' % (self.code.upper(), self.name)).\
            encode('utf-8')

    def __unicode__(self):
        return unicode(self.code)

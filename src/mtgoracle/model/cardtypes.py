from mtgoracle.model import DeclarativeBase
from sqlalchemy import Column, Unicode, Table, ForeignKey


card_type_association = Table('mtgoracle_card_types',
        DeclarativeBase.metadata,
        Column('cardname', Unicode(127), ForeignKey('mtgoracle_cards.name')),
        Column('type', Unicode(15), ForeignKey('mtgoracle_types.name')))

card_subtype_association = Table('mtgoracle_card_subtypes',
        DeclarativeBase.metadata,
        Column('cardname', Unicode(127), ForeignKey('mtgoracle_cards.name')),
        Column('type', Unicode(15), ForeignKey('mtgoracle_subtypes.name')))


class CardType(DeclarativeBase):
    __tablename__ = 'mtgoracle_types'
    name = Column(Unicode(15), primary_key=True, unique=True, nullable=False)

    # {Special methods
    def __repr__(self):
        return ('<Type: %s>' % self.name).encode('utf-8')

    def __unicode__(self):
        return unicode(self.type)


class CardSubtype(DeclarativeBase):
    __tablename__ = 'mtgoracle_subtypes'
    name = Column(Unicode(15), primary_key=True, unique=True, nullable=False)

    # {Special methods
    def __repr__(self):
        return ('<SubType: %s>' % self.name).encode('utf-8')

    def __unicode__(self):
        return unicode(self.type)

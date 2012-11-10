# pymtgoracle

Python library for MtG:Oracle


## Dependencies

* requests
* BeautifulSoup
* SQLAlchemy


## Usage

### Initial Database Scrape

In order to use mymtgoracle, you must first scrape all of the cards from
http://magiccards.info

This can be accomplished by firing up python and issuing the following commands:

    >>> from mtgoracle.scraper import scrape_all
    >>> scrape_all()

This will pull down everything that magiccards.info knows and store it in a
local SQL database. The database is configured in mtgoracle/dbengine.py and
defaults to a sqlite database saved at ~/mtgoracle.sqlite

Scraping might take a little while but you should only have to do it once (or
no more than once each time that pymtgoracle is updated or a new set is
released).

### Initialize Session

Fire up python and initialize the session:

    >>> from mtgoracle.dbengine import get_engine
    >>> from mtgorale.model import *
    >>> init_model(get_engine())

### issue queries/get objects

For now most of the functionality exists by issuing SQLAlchemy queries but a
few of the classes have some utility methods to fetch cards. Once you have a
card, you can examine its attributes.

    >>> pd = Card.by_name(u'Phyrexian Dreadnought')
    >>> print pd.rules
    Trample
    When Phyrexian Dreadnought enters the battlefield, sacrifice it unless you
    sacrifice any number of creatures with total power 12 or greater.
    >>> Card.with_subtype(u'Island')
    [<Card: Hallowed Fountain>,
     <Card: Steam Vents>,
     <Card: Island>,
     <Card: Moonring Island>,
     <Card: Snow-Covered Island>,
     <Card: Breeding Pool>,
     <Card: Watery Grave>,
     <Card: Tropical Island>,
     <Card: Tundra>,
     <Card: Underground Sea>,
     <Card: Volcanic Island>]
    >>> cmc0s = DBSession.query(Card).filter_by(cost=u'0').all()
    >>> len(cmc0s)
    49
    >>> cmc0s[0]
    <Card: Darksteel Relic>
    >>> cmc0s[-1]
    <Card: Urza's Contact Lenses>

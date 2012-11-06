import requests
from BeautifulSoup import BeautifulSoup
from mtgoracle.model import Card, CardSet, CardPrinting, DBSession
import string
import os.path

URL_BASE = 'http://magiccards.info'


def scrape_all():
    from mtgoracle.dbengine import dbPath, get_engine
    from mtgoracle.model import metadata
    dbbak = dbPath + '.bak'
    if os.path.exists(dbbak):
        os.remove(dbbak)
    if os.path.exists(dbPath):
        os.rename(dbPath, dbbak)
    engine = get_engine(path=dbPath, echo=False)
    metadata.create_all(bind=engine)  #@UndefinedVariable @IgnorePep8
    DBSession.configure(bind=engine)
    setdicts = scrape_setdicts()[:5]
    for setdict in setdicts:
        cset = CardSet(**setdict)
        DBSession.add(cset)
        print cset
        carddicts = carddicts_from_setlink(cset.link)
        for carddict in carddicts:
            card = DBSession.query(Card).\
                    filter_by(name=carddict['name']).first()
            if card is None:
                card = Card(name=carddict['name'])
                DBSession.add(card)
                print card
            printing = CardPrinting(setcode=cset.code,
                                    cardname=card.name,
                                    setnumber=carddict['setnum'],
                                    variant=carddict['variant'])
            printing.link = carddict['link']
            printing.artist = carddict['artist']
            DBSession.add(printing)
            print printing
    DBSession.commit()


def scrape_setdicts():
    req = requests.get(URL_BASE + '/sitemap.html')
    soup = BeautifulSoup(req.content)
    en_anchor = soup.find('a', {'name': 'en'})
    en_table = en_anchor.findNext('table')
    en_setlinks = en_table.findAll('a')
    return [setdict_from_setlink(setlink) for setlink in en_setlinks]


def setdict_from_setlink(setlink):
    setdict = {
        'name': setlink.text,
        'code': setlink.parent.find('small').text,
        'link': setlink['href']}
    blockli = setlink.findParents('li')[-1]
    setdict['block'] = blockli.contents[0]
    return setdict


def carddicts_from_setlink(setlink):
    req = requests.get(URL_BASE + setlink)
    soup = BeautifulSoup(req.content)
    card_table = soup.find(text='&#8470;').findParent('table')
    card_rows = card_table.findAll('tr')
    card_header = [h.text for h in card_rows[0].findAll('th')]
    card_rows = card_rows[1:]
    return [carddict_from_row(row, card_header) for row in card_rows]


def carddict_from_row(card_row, card_header):
    raw_card = dict(zip(card_header, card_row.findAll('td')))
    new_card = {
        'name': raw_card['Card name'].text,
        'link': raw_card['Card name'].find('a')['href'],
        'artist': raw_card['Artist'].text
        }
    numcol = raw_card['&#8470;'].text
    if numcol[-1] in string.lowercase:
        new_card['variant'] = string.lowercase.index(numcol[-1])
        numcol = numcol[:-1]
    else:
        new_card['variant'] = -1
    new_card['setnum'] = int(numcol)
    return new_card


if __name__ == '__main__':
    scrape_all()

import requests
from BeautifulSoup import BeautifulSoup
from mtgoracle.model import Card, CardSet

URL_BASE = 'http://magiccards.info'


def scrape_sets():
    req = requests.get(URL_BASE + '/sitemap.html')
    soup = BeautifulSoup(req.content)
    en_anchor = soup.find('a', {'name': 'en'})
    en_table = en_anchor.findNext('table')
    en_setlinks = en_table.findAll('a')
    return [set_from_setlink(setlink) for setlink in en_setlinks]


def set_from_setlink(setlink):
    setdict = {
        'name':setlink.text,
        'code':setlink.parent.find('small').text,
        'link':setlink['href']}
    blockli = setlink.findParents('li')[-1]
    setdict['block'] = blockli.contents[0]
    return CardSet(**setdict)

def get_cards_from_setlink(setlink):
    req = requests.get(URL_BASE + setlink)
    soup = BeautifulSoup(req.content)
    card_table = soup.find(text='&#8470;').findParent('table')
    card_rows = card_table.findAll('tr')
    card_header = [h.text for h in card_rows[0].findAll('th')]
    card_rows = card_rows[1:]
    return [card_from_row(row, card_header) for row in card_rows]

def card_from_row(card_row, card_header):
    raw_card = dict(zip(card_header, card_row.findAll('td')))
    new_card = {
        'setnum': int(raw_card['&#8470;'].text),
        'name': raw_card['Card name'].text,
        'link': raw_card['Card name'].find('a')['href'],
        'artist': raw_card['Artist'].text,
        'cost': raw_card['Mana'].text,
        'rarity': raw_card['Rarity'].text,
        'set': raw_card['Edition'].text,
        }
    typeline = raw_card['Type'].text.split(' ')
    if '/' in typeline[-1]:
        pt = typeline[-1]
        typeline = typeline[:-1]
        new_card['power'], new_card['toughness'] = pt.split('/')
    if u'\u2014' in typeline:
        sti = typeline.index(u'\u2104')
        new_card['subtypes'] = typeline[(sti + 1):]
        typeline = typeline[:sti]
    new_card['supertypes'] = typeline
    return Card(**new_card)

import collections
import bs4
import os
import sqlalchemy
import string
import urllib.parse
import urllib.request

from sqlalchemy import orm

from pymtgoracle.model import base
from pymtgoracle.model import card
from pymtgoracle.model import cardprinting
from pymtgoracle.model import cardset
from pymtgoracle.model import cardtypes


class MagicCardsInfoScraper(object):
  
  URL_BASE = 'http://magiccards.info'
  SET_BLACKLIST = {'UH', 'UG', 'UHAA', 'HHO', 'UQC', 'ARENA'}
  
  def __init__(self, session, verbose=False):
    self.session = session
    self.verbose = verbose
    self._sets = collections.OrderedDict()
    
  def _announce(self, *args):
    if self.verbose:
      try:
        print(*args)
      except UnicodeEncodeError:
        print(*[ascii(arg) for arg in args])

  def setlist(self):
    return self._sets.keys()
      
  def scrape_setlist(self):
    sets_url = self.URL_BASE + '/sitemap.html'
    response = urllib.request.urlopen(sets_url)
    html = response.read()
    html = html.decode('UTF-8').replace('<br>','<br/>')  # workaround for bs4
    soup = bs4.BeautifulSoup(html)
    en_anchor = soup.find('a', {'name': 'en'})
    en_table = en_anchor.findNext('table')
    en_setlinks = en_table.findAll('a')
    for setlink in en_setlinks:
      block = setlink.findParents('li')[-1].contents[0]
      name = setlink.text
      code = setlink.parent.find('small').text.upper()
      link = self.URL_BASE + setlink['href']
      if code in self.SET_BLACKLIST:
        continue
      self._sets[code] = dict(block=block, name=name, code=code, link=link)
      
  def scrape_all(self):
    for set_code in self._sets:
      self.scrape_set(set_code)
      
  def scrape_set(self, set_code):
    set_dict = self._sets[set_code]
    cardset = self._add_cardset(set_dict)
    for printing_dict in self._scrape_printing_dicts(cardset.code):
      self._add_card(printing_dict)
      self._add_printing(printing_dict)
      
  def _add_cardset(self, set_dict):
    cset = self.session.query(cardset.CardSet).filter_by(
        code=set_dict['code']).first()
    if cset is not None:
      return cset
    cset = cardset.CardSet(code=set_dict['code'],
                           name=set_dict['name'],
                           block=set_dict['block'],
                           link=set_dict['link'])
    self._announce('Adding', repr(cset))
    self.session.add(cset)
    return cset
  
  def _scrape_printing_dicts(self, set_code):
    query = dict(q='++e:%s/en' % set_code, v='spoiler', s='issue')
    spoilerlink = self.URL_BASE + '/query?' + urllib.parse.urlencode(query)
    print('Spoiler from', spoilerlink)
    response = urllib.request.urlopen(spoilerlink)
    html = response.read()
    html = html.decode('UTF-8').replace('<br>','<br/>')  # workaround for bs4
    soup = bs4.BeautifulSoup(html)
    cspans = soup.findAll('span')
    for cspan in cspans:
      yield self._printing_dict_from_cspan(cspan)
      
  @classmethod
  def _printing_dict_from_cspan(cls, cspan):
    name = cspan.text
    a_link = cspan.find('a')['href']
    p_rules = cspan.findNextSibling('p', {'class': 'ctext'})
    p_typecost = p_rules.findPreviousSibling('p')
    p_rarity = p_typecost.findPreviousSibling('p')
    p_flavor = p_rules.findNextSibling('p')
    p_art = p_flavor.findNextSibling('p')
    
    _, link_set, link_lang, link_card = a_link.split('/')
    cardlink = '/'.join([cls.URL_BASE, link_set, link_lang, link_card])
    imagelink = '/'.join([cls.URL_BASE, 'scans', link_lang, link_set,
                          link_card.replace('.html', '.jpg')])
    setcode = link_set.upper()
    setnum = link_card.replace('.html', '')
    if setnum[-1] in string.ascii_lowercase:
      variant = string.ascii_lowercase.index(setnum[-1])
      number = int(setnum[:-1])
    else:
      variant = 0
      number = int(setnum)
  
    rules_lines = [r for r in p_rules.find('b').contents
             if isinstance(r, bs4.NavigableString)]
    rules = '\n'.join(rules_lines)
    typeline, costline = [l.strip() for l in p_typecost.text.split(',')]
    types = typeline.split()
  
    if '/' in types[-1]:
      pwr, tgh = types[-1].split('/')
      types = types[:-1]
    else:
      pwr, tgh = None, None
      
    if '\u2014' in types:
      i = types.index('\u2014')
      suptypes = types[:i]
      subtypes = types[i + 1:]
    else:
      suptypes = types
      subtypes = []
      
    if '(Loyalty:' in subtypes:
      i = subtypes.index('(Loyalty:')
      loyalty = int(subtypes[i + 1].strip(')'))
      subtypes = subtypes[:i]
    else:
      loyalty = None
      
    if not costline:
      cost, cmc = '', 0
    elif '(' in costline:
      cost, cmc = costline.split()
      cmc = int(cmc.strip('()'))
    else:
      cost, cmc = costline, 0
      
    rarity = p_rarity.findNext('i').text if p_rarity else 'Special'
    flavor = p_flavor.text if p_flavor.text else None
    artist = p_art.text.replace('Illus. ', '')
      
    return dict(name=name, setcode=setcode, rules=rules, power=pwr,
                toughness=tgh, types=suptypes, subtypes=subtypes, cost=cost,
                cmc=cmc, colorid=None, loyalty=loyalty, link=cardlink,
                imagelink=imagelink, number=number, variant=variant,
                rarity=rarity, flavor=flavor, artist=artist)
    
  def _add_printing(self, printing_dict):
    printing = self.session.query(cardprinting.CardPrinting).filter_by(
        setcode=printing_dict['setcode'], cardname=printing_dict['name'],
        number=printing_dict['number'], variant=printing_dict['variant']).first()
    if printing is not None:
      return printing
    printing = cardprinting.CardPrinting(cardname=printing_dict['name'],
                                         setcode=printing_dict['setcode'],
                                         number=printing_dict['number'],
                                         variant=printing_dict['variant'],
                                         rarity=printing_dict['rarity'],
                                         link=printing_dict['link'],
                                         imagelink=printing_dict['imagelink'],
                                         artist=printing_dict['artist'],
                                         flavor=printing_dict['flavor'])
    self._announce('Adding', repr(printing))
    self.session.add(printing)
    return printing
  
  def _add_card(self, card_dict):
    crd = self.session.query(card.Card).filter_by(
        name=card_dict['name']).first()
    if crd is not None:
      return card
    crd = card.Card(name=card_dict['name'],
                    cmc=card_dict['cmc'],
                    cost=card_dict['cost'],
                    colorid=card_dict['colorid'],
                    rules=card_dict['rules'],
                    power=card_dict['power'],
                    toughness=card_dict['toughness'],
                    loyalty=card_dict['loyalty'])
    for typename in card_dict['types']:
      crd.types.append(self._add_cardtype(typename))
    for subtypename in card_dict['subtypes']:
      crd.subtypes.append(self._add_cardsubtype(subtypename))
    self._announce('Adding', repr(crd))
    self.session.add(crd)
    return crd

  def _add_cardtype(self, typename):
    cardtype = self.session.query(cardtypes.CardType).filter_by(
        name=typename).first()
    if cardtype is not None:
      return cardtype
    cardtype = cardtypes.CardType(name=typename)
    self._announce('Adding', repr(cardtype))
    self.session.add(cardtype)
    return cardtype
  
  def _add_cardsubtype(self, typename):
    cardsubtype = self.session.query(cardtypes.CardSubtype).filter_by(
        name=typename).first()
    if cardsubtype is not None:
      return cardsubtype
    cardsubtype = cardtypes.CardSubtype(name=typename)
    self._announce('Adding', repr(cardsubtype))
    self.session.add(cardsubtype)
    return cardsubtype


def main():
  db_location = './mtgoracle.sqlite'
  db_filename = os.path.expanduser(db_location)
  dbbak_filename = db_filename + '.bak'
  
  if os.path.exists(dbbak_filename):
    os.remove(dbbak_filename)
  if os.path.exists(db_filename):
    os.rename(db_filename, dbbak_filename)
    
  engine = sqlalchemy.create_engine('sqlite:///%s' % db_filename, echo=False)
  base.Base.metadata.create_all(engine)
  
  session_factory = orm.sessionmaker(
      bind=engine, autoflush=True, autocommit=False)
  session = orm.scoped_session(session_factory)
  
  try:
    scraper = MagicCardsInfoScraper(session, verbose=True)
    scraper.scrape_setlist()
    #scraper.scrape_set('ME3')
    scraper.scrape_all()
  except:
    session.rollback()
    raise
  else:
    session.commit()
  finally:
    session.close()

if __name__ == '__main__':
  main()

'''
Created on Aug 9, 2013

@author: gwaksman
'''

from rdflib import Namespace


ORACLE = Namespace('http://www.gwax.com/oracle/')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
MAGICCARDSINFO = Namespace('http://www.magiccards.info/')
MTGSUBTYPE = Namespace('http://www.gwax.com/oracle/subtype#')
MTGSUPERTYPE = Namespace('http://www.gwax.com/oracle/supertype#')
MTGTYPE = Namespace('http://www.gwax.com/oracle/cardtype#')
MTGSET = Namespace('http://www.gwax.com/oracle/cardset/')
MTGCARD = Namespace('http://www.gwax.com/oracle/cardname#')
MTGBLOCK = Namespace('http://www.gwax.com/oracle/cardblock#')
MTGRARITY = Namespace('http://www.gwax.com/oracle/cardrarity#')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

nsdict = {'oracle': ORACLE,
          'owl': OWL,
          'rdf': RDF,
          'rdfs': RDFS,
          'magiccardsinfo': MAGICCARDSINFO,
          'subtype': MTGSUBTYPE,
          'supertype': MTGSUPERTYPE,
          'type': MTGTYPE,
          'set': MTGSET,
          'block': MTGBLOCK,
          'card': MTGCARD,
          'rarity': MTGRARITY,
          'xsd': XSD}

'''
Created on Aug 9, 2013

@author: gwaksman
'''

from mtgoracle.rdf.prefix import RDF, ORACLE, MTGSET, nsdict, MAGICCARDSINFO, \
    XSD, MTGBLOCK, OWL, RDFS, MTGCARD, MTGPRINT, MTGRARITY, MTGSUBTYPE
from mtgoracle.rdf.store import PersistentStore
from mtgoracle.scraper import scrape_setdicts, scrape_printdicts
from rdflib import Literal, URIRef, BNode
from datetime import datetime
import os.path
from mtgoracle.rdf import quote_name


RESET_PERSISTENCE = True
OUTPATH = '.'


def rdfify_set(setdict, setgraph, blockgraph):
    blockuri = MTGBLOCK[quote_name(setdict['block'])]
    if (blockuri, RDF.type, ORACLE.Block) not in blockgraph:
        blocklit = Literal(setdict['block'], datatype=XSD.string)
        blockgraph.add((blockuri, RDF.type, ORACLE.Block))
        blockgraph.add((blockuri, RDFS.label, blocklit))
        blockgraph.add((blockuri, ORACLE.name, blocklit))
    seturi = MTGSET[quote_name(setdict['name'])]
    if (seturi, RDF.type, ORACLE.Set) not in setgraph:
        setlit = Literal(setdict['name'], datatype=XSD.string)
        setgraph.add((seturi, RDF.type, ORACLE.Set))
        setgraph.add((seturi, RDFS.label, setlit))
        setgraph.add((seturi, ORACLE.name, setlit))
        setgraph.add((seturi, MAGICCARDSINFO.enlink, URIRef(setdict['link'])))
        setgraph.add((seturi, MAGICCARDSINFO.setcode, Literal(setdict['code'], datatype=XSD.string)))
        setgraph.add((seturi, ORACLE.block, blockuri))
    return seturi


def rdfify_printing(printdict, printgraph, cardgraph, subtypegraph, seturi):
    print printdict
    carduri = MTGCARD[quote_name(printdict['name'])]
    if (carduri, RDF.type, ORACLE.Card) not in cardgraph:
        cardlit = Literal(printdict['name'], datatype=XSD.string)
        cardgraph.add((carduri, RDF.type, ORACLE.Card))
        cardgraph.add((carduri, RDFS.label, cardlit))
        cardgraph.add((carduri, ORACLE.name, cardlit))
        if printdict['power'] is not None:
            if isinstance(printdict['power'], (int, long)):
                dtype = XSD.integer
            else:
                dtype = XSD.string
            cardgraph.add((carduri, ORACLE.power, Literal(printdict['power'], datatype=dtype)))
        if printdict['toughness'] is not None:
            if isinstance(printdict['toughness'], (int, long)):
                dtype = XSD.integer
            else:
                dtype = XSD.string
            cardgraph.add((carduri, ORACLE.toughness, Literal(printdict['toughness'], datatype=dtype)))
        rulesbag = BNode()
        cardgraph.add((carduri, ORACLE.rules, rulesbag))
        cardgraph.add((rulesbag, RDF.type, RDF.Bag))
        rulenum = 1
        for rule in printdict['rules']:
            rulepred = RDF['_' + str(rulenum)]
            cardgraph.add((rulesbag, rulepred, Literal(rule, datatype=XSD.string)))
            rulenum += 1
        cardgraph.add((carduri, ORACLE.cmc, Literal(printdict['cmc'], datatype=XSD.integer)))
        cardgraph.add((carduri, ORACLE.cost, Literal(printdict['cost'], datatype=XSD.string)))
        if printdict['loyalty'] is not None:
            cardgraph.add((carduri, ORACLE.loyalty, Literal(printdict['loyalty'], datatype=XSD.integer)))
        for typ in printdict['types']:
            pass  # hmm???? inferencing???
        for subtype in printdict['subtypes']:
            suburi = MTGSUBTYPE[subtype]
            if (suburi, RDF.type, ORACLE.Subtype) not in subtypegraph:
                sublit = Literal(subtype, datatype=XSD.string)
                subtypegraph.add((suburi, RDF.type, ORACLE.Subtype))
                subtypegraph.add((suburi, RDFS.label, sublit))
                subtypegraph.add((suburi, ORACLE.identifier, sublit))
            cardgraph.add((carduri, ORACLE.type, suburi))
    printuri = MTGPRINT[quote_name(printdict['setcode'] + '_' + str(printdict['number']))]
    if (printuri, RDF.type, ORACLE.CardPrinting) not in printgraph:
        printgraph.add((printuri, RDF.type, ORACLE.CardPrinting))
        printgraph.add((printuri, ORACLE.card, carduri))
        printgraph.add((printuri, ORACLE.set, seturi))
        printgraph.add((printuri, ORACLE.setNumber, Literal(printdict['number'], datatype=XSD.integer)))
        printgraph.add((printuri, ORACLE.artist, Literal(printdict['artist'], datatype=XSD.string)))
        printgraph.add((printuri, ORACLE.rarity, MTGRARITY[printdict['rarity']]))
        printgraph.add((printuri, MAGICCARDSINFO.enlink, URIRef(printdict['link'])))
        if printdict['flavor'] is not None:
            printgraph.add((printuri, ORACLE.flavor, Literal(printdict['flavor'], datatype=XSD.string)))
    return printuri


def main():
    with PersistentStore(wipe=RESET_PERSISTENCE) as store:
        graph = store.conjunctive_graph()
        print 'Setting up namespaces'
        for name, ns in nsdict.iteritems():
            graph.bind(name, ns)
        print 'Fetching set information'
        setgraph = store.context_graph(MTGSET.graph)
        blockgraph = store.context_graph(MTGBLOCK.graph)
        cardgraph = store.context_graph(MTGCARD.graph)
        printgraph = store.context_graph(MTGPRINT.graph)
        subtypegraph = store.context_graph(MTGSUBTYPE.graph)
        for setdict in scrape_setdicts()[:1]:
            seturi = rdfify_set(setdict, setgraph, blockgraph)
            for printdict in scrape_printdicts(setdict['code'])[:5]:
                printuri = rdfify_printing(printdict, printgraph, cardgraph, subtypegraph, seturi)
        print 'Adding scraping info'
        scrapestr = 'scraping-' + datetime.now().strftime('%Y%m%d')
        scrapeuri = ORACLE[scrapestr]
        graph.bind('', scrapeuri + '#')
        graph.add((scrapeuri, RDF.type, OWL.Ontology))
        graph.add((scrapeuri, OWL.imports, ORACLE['']))
        graph.add((scrapeuri, OWL.versionInfo, Literal('Created with pymtgoracle', datatype=XSD.string)))
        print 'Serializing output'
        outfile = os.path.join(OUTPATH, scrapestr + '.ttl')
        graph.serialize(destination=outfile, format='turtle')
        print 'Done'

if __name__ == '__main__':
    main()

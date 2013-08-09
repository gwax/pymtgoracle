'''
Created on Aug 9, 2013

@author: gwaksman
'''

from mtgoracle.rdf.prefix import RDF, ORACLE, MTGSET, nsdict, MAGICCARDSINFO, \
    XSD, MTGBLOCK
from mtgoracle.rdf.store import PersistentStore
from mtgoracle.scraper import scrape_setdicts
from rdflib import Literal, URIRef
import os.path
from mtgoracle.rdf import quote_name


RESET_PERSISTENCE = True
OUTFILE = os.path.join('.', 'output.ttl')


def main():
    with PersistentStore(wipe=RESET_PERSISTENCE) as store:
        graph = store.conjunctive_graph()
        print 'Setting up namespaces'
        for name, ns in nsdict.iteritems():
            graph.bind(name, ns)
        print 'Fetching set information'
        setgraph = store.context_graph(MTGSET.graph)
        blockgraph = store.context_graph(MTGBLOCK.graph)
        setdicts = scrape_setdicts()
        for setdict in setdicts:
            blockuri = MTGBLOCK[quote_name(setdict['block'])]
            if (blockuri, RDF.type, ORACLE.Block) not in blockgraph:
                blockgraph.add((blockuri, RDF.type, ORACLE.Block))
                blockgraph.add((blockuri, ORACLE.name, Literal(setdict['block'], datatype=XSD.string)))
            seturi = MTGSET[quote_name(setdict['name'])]
            setgraph.add((seturi, RDF.type, ORACLE.Set))
            setgraph.add((seturi, ORACLE.name, Literal(setdict['name'], datatype=XSD.string)))
            setgraph.add((seturi, MAGICCARDSINFO.enlink, URIRef(setdict['link'])))
            setgraph.add((seturi, ORACLE.block, blockuri))
        print 'Serializing output'
        graph.serialize(destination=OUTFILE, format='turtle')
        print 'Done'

if __name__ == '__main__':
    main()

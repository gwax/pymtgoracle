'''
Created on Aug 9, 2013

@author: gwaksman
'''

from mtgoracle.rdf.prefix import RDF, ORACLE, MTGSET, nsdict, MAGICCARDSINFO, \
    XSD, MTGBLOCK, OWL, RDFS
from mtgoracle.rdf.store import PersistentStore
from mtgoracle.scraper import scrape_setdicts
from rdflib import Literal, URIRef, Namespace
from datetime import datetime
import os.path
from mtgoracle.rdf import quote_name


RESET_PERSISTENCE = True
OUTPATH = '.'


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
            blocklit = Literal(setdict['block'], datatype=XSD.string)
            if (blockuri, RDF.type, ORACLE.Block) not in blockgraph:
                blockgraph.add((blockuri, RDF.type, ORACLE.Block))
                blockgraph.add((blockuri, RDFS.label, blocklit))
                blockgraph.add((blockuri, ORACLE.name, blocklit))
            seturi = MTGSET[quote_name(setdict['name'])]
            setlit = Literal(setdict['name'], datatype=XSD.string)
            setgraph.add((seturi, RDF.type, ORACLE.Set))
            setgraph.add((seturi, RDFS.label, setlit))
            setgraph.add((seturi, ORACLE.name, setlit))
            setgraph.add((seturi, MAGICCARDSINFO.enlink, URIRef(setdict['link'])))
            setgraph.add((seturi, ORACLE.block, blockuri))
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

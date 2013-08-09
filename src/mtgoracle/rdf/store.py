'''
Created on Aug 9, 2013

@author: gwaksman
'''

from rdflib import ConjunctiveGraph, Graph
from rdflib.store import NO_STORE, VALID_STORE
from rdflib.plugins.sleepycat import Sleepycat
import shutil
import os.path


class PersistentStore(object):
    def __init__(self, location=os.path.join('.', 'mtgstore'), wipe=False):
        store = Sleepycat()
        if wipe and os.path.exists(location):
            print 'Erasing ' + location
            shutil.rmtree(location)
        rt = store.open(location, create=False)
        if rt == NO_STORE:
            rt = store.open(location, create=True)
        assert rt == VALID_STORE, 'Persistence store is broken'
        print 'Persistent store contains %d statements' % len(store)
        self.__store = store
        return

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__store.close()
        return

    def conjunctive_graph(self):
        return ConjunctiveGraph(self.__store)

    def context_graph(self, context):
        return Graph(self.__store, identifier=context)

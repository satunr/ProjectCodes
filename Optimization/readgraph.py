from networkx import release

from networkx import DiGraph
import scipy



def read(fname):

    G = DiGraph()
    f = open(fname,'r')
    lines = f.readlines()

    for each in lines:
        if 'node' in each:
            n = [int(s) for s in each.split() if s.isdigit()]
            #G.add_node(n)
            #print (n)

    for each in lines:
        if 'edge' in each:
            n = [int(s) for s in each.split() if s.isdigit()]
            #G.add_edge(n[0],n[1])
            print (n[0],n[1])

    #print (G.nodes())
    #print (G.edges())


read('Yeast.gml')

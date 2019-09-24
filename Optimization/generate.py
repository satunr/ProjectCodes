import networkx as nx
import random
import numpy as np
import os

from Optimization.constant import *

def gen(G,si):

    H = G.to_undirected()
    dsum = float(sum([H.degree(u) for u in H.nodes()]))
    #New subgraph
    g = nx.DiGraph()

    #Pick random seed as a starting node
    r = np.random.choice(G.nodes(),1,p = [float(H.degree(u))/float(dsum) for u in G.nodes()])
    print (r)
    g.add_node(int(r[0]))


    while(len(g) < si):

        nset = []

        #List of all neighbors of nodes in g
        for u in g.nodes():
            l = H.neighbors(u)
            nset.extend(l)

        #The nodes in 'nset' are not already present in g
        nset = [u for u in nset if u not in g.nodes()]
        #print ("nset:",len(nset))

        r = random.choice(nset)
        for u in g.nodes():
            if G.has_edge(u,r):
                g.add_edge(u,r)

            if G.has_edge(r,u):
                g.add_edge(r,u)

    h = g.to_undirected()
    if nx.number_connected_components(h) > 1:
        print ("ALARM---")

    return g

'''
G = nx.read_gml('Yeast0.gml')
#G = nx.convert_node_labels_to_integers(G,first_label = 0)

os.chdir('/Users/satyakiroy/PycharmProjects/Main/Optimization/graphs')
for i in range(s):

    print (i)
    g = gen(G, si)

    #print (len(g))
    print (len(g.edges()))

    nx.write_gml(g,'g' + str(i) + '.gml')

'''

import networkx as nx
import numpy as np
import random

import matplotlib.pyplot as plt

def degree_distribution(G):

    mod = max([G.out_degree(u) for u in G.nodes()])
    D = [0.0 for i in range(mod + 1)]

    for u in G.nodes():
        D[G.out_degree(u)] += 1

    plt.plot([i for i in range(mod + 1)],D)
    plt.show()

def motif(G):

    cnt = 0
    for u in G.nodes():
        for v in G.nodes():
            for w in G.nodes():
                if G.has_edge(u,v) and G.has_edge(v,w) and G.has_edge(u,w):
                    cnt += 1

        print (u,cnt)

    return cnt


#G = nx.scale_free_graph(4441)

#print (len(G.nodes()))
#print (len(G.edges()))
#print (motif(G))

H = nx.read_gml('Yeast0.gml')
print (motif(H))


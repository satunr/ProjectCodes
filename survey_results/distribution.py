import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

import os
import numpy as np


mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10

font = {'family':'normal',
        'size':15}

mpl.rc('font',**font)

def dist(G):

    max_deg = max([G.out_degree(u) for u in G.nodes()])
    x = [i for i in range(max_deg + 1)]
    y = [0 for i in range(max_deg + 1)]

    for u in G.nodes():
        y[G.out_degree(u)] += 1


    #plt.plot(x,y)
    plt.scatter(np.log(x),np.log(y),s = 5)
    plt.xlabel('Out-degree')
    plt.ylabel('Frequency')
    plt.savefig('DD.png',dpi = 300)
    plt.show()

G = nx.read_gml('Human_Ordered.gml')

dist(G)

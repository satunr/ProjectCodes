import networkx as nx
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10

font = {'family':'normal',
        'size':15}

mpl.rc('font',**font)


def viz():

    #F_target = [1, 44, 45, 125, 131, 140, 142, 143, 145, 147, 153]
    #F_random = [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4]


    F_random = [2804, 2802, 2799, 2797, 2795, 2793, 2791, 2789, 2787, 2782, 2780]
    F_target = [2804, 2777, 2690, 2688, 2661, 2652, 2622, 2620, 2615, 2612, 2569]

    X = list([0.1 * i for i in range(11)])

    plt.plot(X, F_random, label = 'Random node failure',c = 'green',linewidth = 2)
    plt.plot(X, F_target, label = 'Targeted node failure',c = 'red',linewidth = 2)

    plt.legend()
    plt.xlabel('Percentage of failed nodes')
    plt.ylabel('Size of largest connected component')

    plt.savefig('Failure2.png',dpi = 300)
    plt.show()

def giant(G):

    giant = list(max(nx.connected_component_subgraphs(G), key=len))
    return len(giant)

'''
G = nx.read_gml('Human_Ordered.gml')
G = G.to_undirected()
G = max(nx.connected_component_subgraphs(G), key=len)
n = len(G)
p = 0.001

L = []
#L.append(nx.number_connected_components(G))
L.append(giant(G.copy()))

for i in range(10):

    #Random node failure
    #r = list(np.random.choice(G.nodes(),size = int(p * n),replace = False))

    #Targeted node failure
    S = sum([G.degree(u) for u in G.nodes()])
    r = list(np.random.choice(sorted(G.nodes()),size = int(p * n),replace = False,p = [float(G.degree(u))/S for u in sorted(G.nodes())]))

    G.remove_nodes_from(r)
    H = G.to_undirected()

    #L.append(nx.number_connected_components(H))
    L.append(giant(H.copy()))

print (L)
'''
viz()


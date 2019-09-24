import networkx as nx
import os

def density(G):

    e = float(len(G.edges()))
    n = float(len(G))

    if e == 0 or e == 1:
        return 0

    return float(n * (n - 1))/float(e)

def clustering(G):

    H = G.to_undirected()
    return nx.average_clustering(H)

def efficiency(G):

    d = 0.0
    den = 0.0

    for u in G.nodes():
        for v in G.nodes():
            if not nx.has_path(G,u,v) or u == v:
                continue
            d += 1.0/float(nx.shortest_path_length(G,u,v))
            den += 1.0

    if den == 0:
        return  0

    return float(d)/float(den)


def findFitness(gset,i):

    g = gset[i]
    f = [i]
    f.append(clustering(g))
    f.append(efficiency(g))
    f.append(density(g))

    return f



import networkx as nx
import numpy as np
import pickle, math
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c

def distribution(G):
    x = np.asarray([1000, 3250, 5500, 10000, 32500, 55000, 77500, 100000, 200000])
    y = np.asarray([1100, 500, 288, 200, 113, 67, 52, 44, 5])

    sol1 = curve_fit(func_powerlaw, x, y, maxfev=2000)

    print (sol1)

def show(G,EMC):

    plt.scatter([G.out_degree(u) for u in G.nodes()],[EMC[u] for u in G.nodes()],s = 3)
    plt.show()

def remove(G,EMC,s,removeFraction,LT):

    n = removeFraction * len(G)
    H = G.to_undirected()
    L = []

    for i in range(int(n)):

        md = max([H.degree(u) for u in H.nodes()])
        for u in H.nodes():
            if H.degree(u) == md:

                for v in LT[u]:
                    EMC[v] = EMC[v] - 1
                break

        H.remove_node(u)

        s = s - EMC[u]

        if EMC[u] <= 0:
            break

        L.append(s)

    return L

def motif(G):

    EMC = {}
    for u in G.nodes():
        EMC[u] = 0

    s = 0

    #Set of edges affected by removal of current edge
    LT = [[] for i in range(len(G.nodes()))]

    for u in G.nodes():
        print (u)
        for v in G.nodes():
            if v == u:
                continue

            for w in G.nodes():
                if w == v or w == u:
                    continue

                if G.has_edge(u,v) and G.has_edge(v,w) and G.has_edge(u,w):
                    EMC[u] += 1
                    EMC[v] += 1
                    EMC[w] += 1
                    s += 1

                    LT[u].extend([v,w])
                    LT[v].extend([u,w])
                    LT[w].extend([u,v])


    return EMC,LT,s


def scale(n):

    G = nx.DiGraph()
    G.add_edges_from([(0,1), (1,2), (2,3), (3,0)])
    ID = 3

    m = 5

    PA = [0,1,2,3]

    while(len(G) < n):

        G.add_node(ID)
        for i in range(m):
            u = np.random.choice(PA)
            PA.append(u)
            G.add_edge(u,ID)

        ID = ID + 1
    return G

'''
removeFraction = 0.05

G = nx.read_gml('scale.gml')

N = sorted(G.nodes())
EMC,LT,s = motif(G)

L = remove(G,EMC,s,removeFraction,LT)
print (L)
'''

'''
#G = nx.read_gml('Yeast0.gml')


G = scale(1000,)
EMC,LT,s = motif(G)

pickle.dump(EMC, open("EMC_SCALE.p", "wb" ))
pickle.dump(LT, open("LT_SCALE.p", "wb" ))

show(G,EMC)

'''

G = nx.read_gml('Yeast0.gml')

distribution(G)


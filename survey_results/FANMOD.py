import networkx as nx

def f(G):

    s = ''
    for e in G.edges():
        s += str(e[0]) + '\t' + str(e[1]) + '\n'

    return s

G = nx.read_gml('Human_Ordered.gml')
s = f(G)

f = open('Human_FANMOD.txt','w')
f.write(s)


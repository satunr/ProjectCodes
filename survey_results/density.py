import networkx as nx

def D(G):

    n = len(G)
    e = len(G.edges())

    return float(e)/float(n * (n - 1))

G_H = nx.read_gml('Human_Ordered.gml')
G_M = nx.read_gml('Mouse_Ordered.gml')

print ('Human:',D(G_H))
print ('Mouse:',D(G_M))

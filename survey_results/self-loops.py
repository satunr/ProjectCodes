import networkx as nx

def sl(G):

    return len([e for e in G.edges() if e[0] == e[1]])

G = nx.read_gml('Mouse_Ordered.gml')

print ('self-loops:',sl(G))
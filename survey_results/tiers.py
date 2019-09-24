import networkx as nx

def edge_distribution(G, t1, t2, t3):

    E_12 = 0.0
    E_13 = 0.0
    E_22 = 0.0
    E_23 = 0.0

    for e in G.edges():

        if e[0] in t1 and e[1] in t2:
            E_12 += 1

        if e[0] in t1 and e[1] in t3:
            E_13 += 1

        if e[0] in t2 and e[1] in t2:
            E_22 += 1

        if e[0] in t2 and e[1] in t3:
            E_23 += 1

    return float(E_12)/float(len(G.edges())), float(E_13)/float(len(G.edges())), float(E_22)/float(len(G.edges())), \
           float(E_23)/float(len(G.edges()))

def tiers1(G):

    t1, t2, t3 = [], [], []

    for u in G.nodes():

        if G.in_degree(u) == 0:
            t1.append(u)
        elif G.out_degree(u) == 0:
            t3.append(u)
        else:
            t2.append(u)

    return t1, t2, t3, float(len(t1))/float(len(G)), float(len(t2))/float(len(G)), float(len(t3))/float(len(G))

'''
G_H = nx.read_gml('Human_Ordered.gml')
G_M = nx.read_gml('Mouse_Ordered.gml')

t1, t2, t3, p1, p2, p3 = tiers(G_H)
#print (p1, p2, p3)
E_12, E_13, E_22, E_23 = edge_distribution(G_H, t1, t2, t3)
print (E_12, E_13, E_22, E_23)

t1, t2, t3, p1, p2, p3 = tiers(G_M)
#print (p1, p2, p3)
E_12, E_13, E_22, E_23 = edge_distribution(G_M, t1, t2, t3)
print (E_12, E_13, E_22, E_23)
'''
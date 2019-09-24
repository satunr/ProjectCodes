import networkx as nx

def findTiers(G):

    t1 = []
    t2 = []
    t3 = []

    for u in G.nodes():

        if G.out_degree(u) > 0 and G.in_degree == 0:
            t1.append(u)
        elif G.out_degree(u) > 0 and G.in_degree > 0:
            t2.append(u)
        else:
            t3.append(u)


    return t1,t2,t3

#G = nx.read_gml('Yeast0.gml')

#t1,t2,t3 = findTiers(G)
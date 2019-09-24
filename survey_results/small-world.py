import networkx as nx

def tiers(G):

    t1, t2, t3 = [], [], []

    for u in G.nodes():

        if G.in_degree(u) == 0:
            t1.append(u)
        elif G.out_degree(u) == 0:
            t3.append(u)
        else:
            t2.append(u)

    return t1, t2, t3

def diameter(G):

    G = G.to_undirected()
    G = max(nx.connected_component_subgraphs(G), key=len)

    print (len(G),len(G.edges()))

    return nx.diameter(G)

def shortest_path(G,t1, t2, t3):

    P = 0.0
    S = 0.0
    for u in t1:
        for v in t3:

            if nx.has_path(G,u,v):
                S += nx.shortest_path_length(G,u,v)
                P += 1.0

    return S/P

G_E = nx.read_gml('Ecoli-Original.gml')
t1, t2, t3 = tiers(G_E)
print ('Ecoli:',diameter(G_E.copy()),shortest_path(G_E.copy(),t1, t2, t3))

G_Y = nx.read_gml('Yeast-Original.gml')
t1, t2, t3 = tiers(G_Y)
print ('Yeast:',diameter(G_Y.copy()),shortest_path(G_Y.copy(),t1, t2, t3))

G_H = nx.read_gml('Human_Ordered.gml')
t1, t2, t3 = tiers(G_H)
print ('Human:',diameter(G_H.copy()),shortest_path(G_H.copy(),t1, t2, t3))

G_M = nx.read_gml('Mouse_Ordered.gml')
t1, t2, t3 = tiers(G_M)
print ('Mouse:',diameter(G_M.copy()),shortest_path(G_M.copy(),t1, t2, t3))



import networkx as nx

def motifs(G):

    C = 0
    M = []
    for u in sorted(G.nodes()):
        print (u)
        for v in G.nodes():
            if v == u:
                continue
            for w in G.nodes():
                if w == u or w == v:
                    continue

                if G.has_edge(u,v) and G.has_edge(v,w) and G.has_edge(u,w):
                    C += 1
                    M.append((u,v,w))


    return C,nx.average_clustering(G.to_undirected()),M

'''
G = nx.read_gml('Mouse_Ordered.gml')
print (motifs(G))
input('')

G_R = nx.erdos_renyi_graph(n = len(G),p = 0.0010,directed = True)
print (motifs(G_R))
'''

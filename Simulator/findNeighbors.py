
def findN(G,ID):
    ind = []
    out = []
    for i in G.nodes():
        if G.has_edge(i, ID):
            ind.append(i)
        elif G.has_edge(ID, i):
            out.append(i)


    return ind,out
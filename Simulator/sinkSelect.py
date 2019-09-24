

def sinkSelector(G):

    sink = []
    for i in G.nodes():

        if G.out_degree(i) == 0:
            sink.append(i)

    return sink
import networkx as nx
import pickle
from Simulator.sinkSelect import *
from Simulator.format import *

#Generate network graph
def generateG():
    #Graph variables
    #G = nx.DiGraph()
    #G.add_edges_from([(0,1),(2,1),(3,1),(4,1),(5,2),(6,3),(3,7)])

    G = nx.read_gml('g2-0.gml')
    #G = G.reverse(copy = True)

    N = len(G.nodes())

    h = pickle.load(open("hn0.p", "rb"))
    s = pickle.load(open("sh0.p", "rb"))

    #sink = sinkSelector(G)
    sink = []
    sink.extend(h)
    #sink.extend(s)
    print (len(G))
    print (len(sink))
    print ("List of sink nodes:",sink,"\n")
    p = NewPacket()

    return G,N,sink,p

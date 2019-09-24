import networkx as nx
import itertools, math
import operator
import matplotlib.pyplot as plt

from scipy.spatial.distance import cosine
from sklearn.model_selection import KFold


def PA(H,u,v):

    #J = H.to_undirected()
    return float(H.out_degree(u) * (H.in_degree(v) + 1))/float(math.pow(len(H) - 1,2))
    #return float(J.degree(u) * J.degree(v))/float(math.pow(len(H) - 1,2))

    #return abs(J.degree(u) - J.degree(v))

'''
def CN(H, u, v):

    #J = H.to_undirected()
    if J.degree(u) == 0 or J.degree(v) == 0:
        return 0

    return float(len([w for w in J.neighbors(u) if w in J.neighbors(v)]))/float(J.degree(u) * J.degree(v))
'''

def PACN(H, u, v, w):
    return w * PA(H,u,v) + (1.0 - w) * CN(H,u,v)

#CONSTANTS
k = 7
repeat = 1
#G = nx.read_gml('Yeast0.gml')
G = nx.read_gml('g1.gml')
print (nx.is_directed(G))

print (len(G.edges()))
E = G.edges()
how_many = 100

w = 0.5
C = list(itertools.permutations(G.nodes(), 2))
print (C)

i = 0

while (i < repeat):

    print ("i = ",i)

    kf = KFold(n_splits = k)

    #j = 0
    for train_index, test_index in kf.split(E):

        score = 0.0

        #print("j = ", j )

        # Train edges
        TRe = []
        # Testing edges
        TEe = []

        TRe.extend([E[z] for z in train_index])
        TEe.extend([E[z] for z in test_index])

        print("Size of TRAIN set:", len(train_index), "Size of TEST test:", len(test_index))

        #Create a reduced graph
        H = nx.DiGraph()
        H.add_nodes_from(G.nodes())
        H.add_edges_from(TRe)

        #print ("HERE1")

        #Prediction
        PR = {}

        for e in C:
            if e not in TRe:
                PR[e] = PA(H,e[0],e[1])

        PR = sorted(PR, key=PR.get,reverse = True)
        PR = PR[:how_many]

        for y in PR:
            if y in TEe:
                score += 1

        print (score)
        #print ("HERE2")

        #j = j + 1

    i = i + 1

#print ("Similarity score PA:",float(score)/float(repeat * k))



'''
B = nx.read_gml('scale.gml')
for e in B.edges():
    plt.scatter(B.degree(e[0]),B.degree(e[1]),s = 1,color = 'r')

plt.show()
'''




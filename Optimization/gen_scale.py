import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from multiprocessing import Pool

'''
G = nx.scale_free_graph(n = 200)
nx.write_gml(G,'scale.gml')

'''

def f(L):

    indices = L[0]
    G = L[1]
    N = L[2]
    i = L[3]
    mod = L[4]
    mid = L[5]
    H = L[6]

    f = [(0.0, 0.0) for i in range((mod + 1) * (mid + 1))]

    for u in N[indices[i]:indices[i + 1]]:

        if i == 0:
            print (u)
        for v in G.nodes():

            '''
            #Preferential Attachment
            num = f[G.out_degree(u) * G.in_degree(v)][0]
            den = f[G.out_degree(u) * G.in_degree(v)][1]
            den += 1.0
            if (u, v) in G.edges():
                num += 1.0
            f[G.out_degree(u) * G.in_degree(v)] = (num, den)
            '''

            #Common Neighbors
            c = len([w for w in H.neighbors(u) if w in H.neighbors(v)])
            num = f[c][0]
            den = f[c][1]
            den += 1.0
            if (u, v) in G.edges():
                num += 1.0

            f[c] = (num,den)

    return f

G = nx.read_gml('scale.gml')
H = G.to_undirected()

mod = max([G.out_degree(u) for u in G.nodes()])
mid = max([G.in_degree(u) for u in G.nodes()])
F = [(0.0, 0.0) for i in range((mod + 1) * (mid + 1))]

N = G.nodes()
#indices = [0,1100,2200,3333,len(G.nodes())]
indices = [0,50,100,150,len(G.nodes())]

cores = 4
po = Pool(processes = cores)

fS = po.map(f,[[indices,G,N,i,mod,mid,H] for i in range(cores)])

for each in fS:
    for j in range(len(F)):
        num = F[j][0] + each[j][0]
        den = F[j][1] + each[j][1]
        F[j] = (num,den)


GG = [float(each[0] + 1)/float(each[1] + 1) for each in F if each[1] != 0]
divide = [F.index(each) for each in F if each[1] != 0]

plt.scatter(divide,GG,s = 3,c = 'red')
plt.show()


print (np.corrcoef(divide, GG)[0, 1])
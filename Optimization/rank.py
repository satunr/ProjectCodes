import networkx as nx
import math

from multiprocessing import Pool


def f(L):

    indices = L[0]
    G = L[1]
    N = L[2]
    i = L[3]
    mod = L[4]
    mid = L[5]
    H = L[6]

    pal = {}
    cnl = {}
    pacnl = {}

    for u in N[indices[i]:indices[i + 1]]:
        for v in G.nodes():
            p = (G.out_degree(u) * G.in_degree(v)) / float(mod * mid)
            pal[(u, v)] = p

            c = len([w for w in H.neighbors(u) if w in H.neighbors(v)]) / float(n - 1)
            cnl[(u, v)] = c

            pacnl[(u, v)] = p * c

    return [pal,cnl,pacnl]

G = nx.read_gml('Yeast0.gml')
n = len(G)
H = G.to_undirected()
cores = 4
N = sorted(G.nodes())
indices = [i * int(n/cores) for i in range(cores)]
indices.append(n)

print (indices)
po = Pool(processes = cores)

PA = {}
CN = {}
PACN = {}

mod = max([G.out_degree(u) for u in G.nodes()])
mid = max([G.in_degree(u) for u in G.nodes()])
w = 0.8


fS = po.map(f,[[indices,G,N,i,mod,mid,H] for i in range(cores)])

for each in fS:

    PA.update(each[0])
    CN.update(each[1])
    PACN.update(each[2])

#Rank nodes by scores

pa = sorted(PA.items(), key=lambda x: x[1],reverse = True)
pa = [each[0] for each in pa]

cn = sorted(CN.items(), key=lambda x: x[1],reverse = True)
cn = [each[0] for each in cn]

pacn = sorted(PACN.items(), key=lambda x: x[1],reverse = True)
pacn = [each[0] for each in pacn]

#Verify
precision_pa = 0.0
precision_cn = 0.0
precision_pacn = 0.0


for e in G.edges():

    if pa.index(e) <= len(G.edges()):
        precision_pa += float(1.0)/len(G.edges())

    if cn.index(e) <= len(G.edges()):
        precision_cn += float(1.0)/len(G.edges())

    if pacn.index(e) <= len(G.edges()):
        precision_pacn += float(1.0)/len(G.edges())

print (precision_pa)
print (precision_cn)
print (precision_pacn)

import networkx as nx
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from Survey_results.motifs import *
from Survey_results.tiers import *
from itertools import permutations,combinations

mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10

font = {'family':'normal',
        'size':15}

mpl.rc('font',**font)

def path_centrality(G):

    PC = {u: 0 for u in G.nodes()}

    for u in sorted(t1):
        for v in sorted(t3):

            print(u, v)
            P = nx.all_simple_paths(G, source=u, target=v, cutoff=5)
            for p in P:
                for w in p[1:-1]:
                    PC[w] += 1

    return PC

def sort(x,y):

    for i in range(len(x) - 1):
        for j in range(i + 1,len(x)):

            if x[i] > x[j]:
                temp = x[i]
                x[i] = x[j]
                x[j] = temp

                temp = y[i]
                y[i] = y[j]
                y[j] = temp

    return x,y

def maps(X,Y):
    z = np.polyfit(X, Y, 2)
    p = np.poly1d(z)

    plt.plot([pt for pt in X],[p(pt) for pt in X])

def check_independent(p_1, p_2):

    p_1 = p_1[1:-1]
    p_2 = p_2[1:-1]

    if len([u for u in p_1 if u in p_2]) > 0:
        return False

    return True

def independent_paths(G,t1,t2,t3):

    IPC = {u:0 for u in G.nodes()}

    for u in t1:
        print (u)
        for v in t3:
            ipc = {u:0 for u in G.nodes()}
            P = list(nx.all_simple_paths(G,source = u,target = v,cutoff = 5))

            C = combinations(range(len(P)),2)
            #print ('C:',list(C))

            for c in list(C):

                if check_independent(P[c[0]],P[c[1]]):
                    for w in P[c[0]][1:-1]:
                        ipc[w] = 1
                    for x in P[c[1]][1:-1]:
                        ipc[x] = 1

            for y in ipc.keys():
                IPC[y] += ipc[y]

    return IPC

G = nx.read_gml('Human_Ordered.gml')
t1, t2, t3, _, _, _ = tiers1(G)

#_,_,M = motifs(G)
#pickle.dump(M,open('Motif_human.p','wb'))

# IPC = independent_paths(G,t1,t2,t3)
# print (IPC)
# pickle.dump(IPC,open('IPC_human.p','wb'))

'''
print (len(t1),len(t2),len(t3))

#Path centrality
PC = path_centrality(G)
pickle.dump(PC,open('PC_human.p','wb'))
'''


M = pickle.load(open('Motif_human.p','rb'))
PC = pickle.load(open('IPC_human.p','rb'))

print (PC)

NMC = {u:0 for u in G.nodes()}
for m in M:
    NMC[m[0]] += 1
    NMC[m[1]] += 1
    NMC[m[2]] += 1

X = [NMC[u] for u in sorted(G.nodes())]
Y = [PC[u] for u in sorted(G.nodes())]

X,Y = sort(X,Y)
maps(X,Y)

plt.scatter(X,Y,s = 4,color = 'black')
plt.xlabel('Node motif centrality')
plt.ylabel('Independent path centrality')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.savefig('IPC.png',dpi = 300)
plt.show()

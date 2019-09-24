import numpy as np
import networkx as nx
import random, math,operator

from constant import *
from findF import *
from generate import *
from copy import deepcopy

from multiprocessing import Pool

Outside_gset = []

def reorganize(Fn,gset,o):

    FN = []
    GSET = []

    for i in range(len(Fn)):

        index = Fn[i][0]
        GSET.append(gset[index])

        new = [i]
        for j in range(o):
            new.append(Fn[i][j + 1])

        FN.append(new)

    return FN,GSET

def checkConnectivity(cg, u):

    hg = nx.DiGraph()
    hg.add_nodes_from(cg.nodes())
    hg.add_edges_from(cg.edges())

    hg.remove_node(u)
    if nx.is_connected(hg.to_undirected()):
        return True

    return False

def mutation(cg, GO, mr):

    for u in cg.nodes():

        r = random.uniform(0,1)
        if r < mr:

            if not checkConnectivity(cg, u):
                continue

            cg.remove_node(u)
            nlist = []
            for v in cg.nodes():
                nlist.extend(GO.neighbors(v))

            new_node = random.choice([v for v in nlist if v not in cg.nodes()])
            cg.add_node(new_node)

            for v in cg.nodes():
                if GO.has_edge(v,new_node):
                    cg.add_edge(v,new_node)
                if GO.has_edge(new_node,v):
                    cg.add_edge(new_node,v)

    return cg


def max_edge_remove(cG,M,si):

    #New subgraph
    nG = nx.DiGraph()

    #Pick random seed as a starting node
    r = random.choice(cG.nodes())
    #print ("r:",r)
    nG.add_node(r)

    d = {e : M[e[0]][e[1]] for e in cG.edges() if e not in nG.edges() and (e[0] in nG.nodes() or e[1] in nG.nodes())}

    while(len(nG) < si):

        #Edge with maximum score
        e = max(d, key = d.get)

        new_node = -1
        if e[0] not in nG.nodes():
            new_node = e[0]
        elif e[1] not in nG.nodes():
            new_node = e[1]

        if new_node >= 0:
            for f in [f for f in cG.edges() if f not in d.keys()]:
                if new_node == f[0] or new_node == f[1]:
                    d[f] = M[f[0]][f[1]]

        d.pop(e, None)
        nG.add_edge(e[0],e[1])

    h = nG.to_undirected()
    if nx.number_connected_components(h) > 1:
        print ("ALARM---")

    return nG

def crossover(GO,G1,G2,si,M):

    #Define combined graph
    cG = nx.DiGraph()
    cG.add_nodes_from([u for u in GO.nodes() if u in G1.nodes() or u in G2.nodes()])

    E = [e for e in GO.edges() if e in G1.edges() or e in G2.edges()]
    cG.add_edges_from(E)

    #return gen(cG,si)
    return max_edge_remove(cG,M,si)


def f(I):

    global Outside_gset

    print (len(Outside_gset))

    #gset = I[0]
    F = I[0]
    si = I[1]
    GO = I[2]
    M = I[3]
    mr = I[4]
    indexing = I[5]
    p = I[6]

    i = 0
    new_F = []
    new_gset = []

    while (i < indexing):

        #Choose the two parents
        parents = []

        #Choose a random graph
        c = random.choice(range(si))

        #Choose a random value between 0 and 1
        r = random.uniform(0, 1)
        if r < p * math.pow((1.0 - p), c):

            g1 = Outside_gset[F[c][0]]
            parents.append(g1)

            c = random.choice(range(si))
            r = random.uniform(0, 1)


            if r < p * math.pow((1.0 - p), c):
                g2 = Outside_gset[F[c][0]]
                if len([u for u in g1.nodes() if u in g2.nodes()]) > 0:
                    parents.append(g2)

                    cg = crossover(GO, parents[0], parents[1], si, M)
                    cg = mutation(cg,GO,mr)
                    new_gset.append(cg)
                    f = findFitness(new_gset, new_gset.index(cg))
                    new_F.append(f)

                    i = i + 1

    return [new_F,new_gset]


def tournament2(gset,F, p, K, si, GO, M, s, cores,po):

    global Outside_gset

    #Number of iterations in each core.py
    indexing = int(K/cores)

    Outside_gset = deepcopy(gset)

    I = [F,si,GO,M,mr,indexing,p]

    C = po.map(f, [I for i in range(cores)])

    for i in range(cores):

        L = C[i]
        for each in L[0]:
            F.append(each)
        for each in L[1]:
            gset.append(each)

    return F, gset


def tournament1(gset,F,prob,K,si,GO,M,s,cores,po):

    P = [prob * math.pow((1.0 - prob), i) for i in range(len(F))]
    P = [float(each)/float(sum(P)) for each in P]

    k = 0
    while(k < K):

        parents = np.random.choice(range(s), 2, p = P)

        g1 = gset[F[parents[0]][0]]
        g2 = gset[F[parents[1]][0]]

        if len([u for u in g1.nodes() if u in g2.nodes()]) > 0:

            cg = crossover(GO, g1, g2, si, M)
            cg = mutation(cg,GO,mr)
            gset.append(cg)
            f = findFitness(gset, gset.index(cg))
            F.append(f)

            k = k + 1

    return F,gset


def tournament(gset,F,p,K,si,GO,M,s,cores,po):

    # gset is the set of graphs
    # Here F is the initial population
    # p is the probability of selection of each individual
    # K is the size of the tournament

    i = 0
    while (i < K):

        #Choose the two parents
        parents = []

        #Choose a random graph
        c = random.choice(range(si))

        #Choose a random value between 0 and 1
        r = random.uniform(0, 1)
        if r < p * math.pow((1.0 - p), c):

            g1 = gset[F[c][0]]
            parents.append(g1)

            c = random.choice(range(si))
            r = random.uniform(0, 1)


            if r < p * math.pow((1.0 - p), c):
                g2 = gset[F[c][0]]
                if len([u for u in g1.nodes() if u in g2.nodes()]) > 0:
                    parents.append(g2)

                    cg = crossover(GO, parents[0], parents[1], si, M)
                    cg = mutation(cg,GO,mr)
                    gset.append(cg)
                    f = findFitness(gset, gset.index(cg))
                    F.append(f)

                    i = i + 1
    return F,gset

def sort(i,f):

    l = len(f)
    # Sort the population by the i-th objective
    arrange = [z for z in range(l)]

    for j in range(l - 1):

        for k in range(j + 1, l):

            if f[arrange[k]][i + 1] > f[arrange[j]][i + 1]:
                t = arrange[j]
                arrange[j] = arrange[k]
                arrange[k] = t

    #print ("Show sorted list:",[F[arrange[k]][i + 1] for k in range(l)])
    return arrange

def crowding(f,o):

    l = len(f)

    #print (f)

    #Crowding distance for each individual
    d = [0.0 for i in range(l)]

    for i in range(o):
        arrange = sort(i,f)
        d[arrange[0]] += float('inf')
        d[arrange[-1]] += float('inf')

        for j in range(1,l - 1):
            d[j] = d[j] + (f[arrange[j - 1]][i + 1] - f[arrange[j + 1]][i + 1])

    return d

def isDominated(e,F):

    for compare in F:

        if compare == e:
            continue

        #Difference list between fitness scores of 'compare' and 'e'
        dlist = [(compare[i] - e[i]) for i in range(len(compare))]

        #Check if any entry is negative. A negative entry indicates the domination is nullified
        if sum(n < 0 for n in dlist[1:]) > 0:
            continue

        #Is dominated
        if sum(n > 0 for n in dlist[1:]) > 0:
            return True

    return False

def findCurrent(F):

    f = []
    for each in F:
        if not isDominated(each,F):
            f.append(each)

    return [each for each in F if each not in f],f

def findParetoFronts(F):

    Fronts = []

    while(len(F) > 0):

        #current front
        F,f = findCurrent(F)
        Fronts.append(f)

    return Fronts


#---NSGA ALGORITHM----

def nsga(gset,F,iterate,s,o,GO,M,cores,po):

    # New population
    Q = []
    Q.extend(F)

    ctr = 0
    FitnessAccount = []

    Fn = []

    #Each iteration
    while(ctr < iterate):

        print ('---',ctr)

        #Determine Fronts
        Fronts = findParetoFronts(Q)
        print ("Size of each fronts: ",[len(each) for each in Fronts])

        #Next Population Parents
        Fn = []

        i = 0
        while(i < len(Fronts)):

            #Population in current front
            FrontP = Fronts[i]

            #Calculate crowding distance of the individuals in FrontP
            c = crowding(FrontP, o)

            #Sort the population indices by decreasing crowding distance
            c = list(np.argsort(c))
            c = c[::-1]

            for j in range(len(c)):
                Fn.append(FrontP[c[j]])

            i = i + 1

        Fn = Fn[:s]

        Fn,gset = reorganize(Fn,gset,o)
        print ("See this:",len(Fn),len(gset))

        f1 = sum([float(each[1]) / float(len(Fn)) for each in Fn])
        f2 = sum([float(each[2]) / float(len(Fn)) for each in Fn])
        f3 = sum([float(each[3]) / float(len(Fn)) for each in Fn])
        FitnessAccount.append((f1,f2,f3))

        print ("Population size:", len(Fn))
        print ("Average fitness:", f1,f2,f3)

        #Apply crossover and mutation to declare new population
        Q = tournament2(gset,Fn, 0.2 ,int(len(Fn)/1.0),si,GO,M,s,cores,po)
        ctr += 1


    return Fn,gset,FitnessAccount

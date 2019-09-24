import networkx as nx
import random
import math
import numpy as np
import os,time
import pickle

from Optimization.show import *
from Optimization.constant import *
from Optimization.findF import *
from Optimization.NSGA import *

'''
#Complete graph
GO = nx.read_gml('Yeast0.gml')
#GO = nx.convert_node_labels_to_integers(GO,first_label = 0)
HO = GO.to_undirected()

#Average degree of HO
d = float(sum([HO.degree(u) for u in HO.nodes()]))/float(len(HO))

M = [[0.0 for u in GO.nodes()] for v in GO.nodes()]
for u in HO.nodes():
    for v in HO.nodes():

        if v < u:
            continue

        nu = HO.neighbors(u)
        nv = HO.neighbors(v)
        C = [w for w in nu if w in nv]

        M[u][v] = len(C) + (e * float(len(nu) * len(nv)) /float(d))
        M[v][u] = len(C) + (e * float(len(nu) * len(nv)) / float(d))

#nx.write_gml(GO,'Yeast0.gml')
pickle.dump(M, open("M.p", "wb"))

'''
M = pickle.load(open("M.p", "rb"))
GO = nx.read_gml('Yeast0.gml')

#Calculate fitness of initial population
curr = os.getcwd()
os.chdir('/Users/satyakiroy/PycharmProjects/Main/Optimization/graphs')

gset = []
for i in range(s):

    g = nx.read_gml('g' + str(i) + '.gml')
    gset.append(g)

os.chdir(curr)

#Fitness F is a list where each entry is individual denoted by [individual id,fitness1,fitness2,...]
#Fronts is a list where i-th entry is set of the individuals in the i-th front

F = []
for i in range(len(gset)):
    f = findFitness(gset,i)
    F.append(f)

#print (len(F))

t0 = time.time()
F,gset,FitnessAccount = nsga(gset,F,iterate,s,o,GO,M,cores,po)

print ("Time taken:",time.time() - t0)

os.chdir('/Users/satyakiroy/PycharmProjects/Main/Optimization/outgraphs')

for i in range(len(F)):

    g = gset[F[i][0]]
    nx.write_gml(g,'g' + str(i) + '.gml')

os.chdir(curr)
pickle.dump(FitnessAccount, open("FitnessAccount.p", "wb"))
#viz(FitnessAccount)






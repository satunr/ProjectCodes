import os
import networkx as nx
import matplotlib.pyplot as plt

def deg(G):

    m_id = max([G.in_degree(u) for u in G.nodes()])
    id = [0.0 for i in range(m_id + 1)]

    for u in G.nodes():
        id[G.in_degree(u)] += 1

    return [i for i in range(m_id + 1)],[float(each)/float(sum(id)) for each in id]


os.chdir('graphs')
colorlist = ['r','g','b','violet','black']
for ii in range(4,5):

    ss = (ii + 2) * 50

    '''
    G = nx.read_gml('GBD' + str(ss) + '.gml')
    X,Y = deg(G)
    plt.plot(X,Y,linewidth = 2,color = 'r')


    G = nx.read_gml('O' + str(ss) + '.gml')
    X,Y = deg(G)
    plt.plot(X,Y,linewidth = 2,color = 'g')

    '''
    G = nx.read_gml('refG' + str(ss) + '.gml')
    X,Y = deg(G)
    plt.plot(X,Y,linewidth = 2,color = 'b')


plt.xlabel('Out-degree')
plt.ylabel('Normalized frequency')
plt.show()


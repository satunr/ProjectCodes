import networkx as nx


fname = 'human.tsv'
f = open(fname,'rb')

L = f.readlines()

P = 0.0
N = 0.0
U = 0.0

for l in L:

    l = str(l)

    if 'Unknown' in l or '+-' in l:
        U += 1
    elif 'Activation' in l or '+' in l:
        P += 1
    elif 'Repression' in l or '-' in l:
        N += 1

print (P/(P + N + U),N/(P + N + U),U/(P + N + U))




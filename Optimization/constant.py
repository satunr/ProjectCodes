from multiprocessing import Pool

#Number of iterations
iterate = 10

#Size of population
s = 300

#Number of objectives
o = 3

#Size of each individual
si = 100

#Mutation Rate
mr = 0.1

#number of cores
cores = 4

#weight factor
e = 0.1

po = Pool(processes=cores)

gset = []


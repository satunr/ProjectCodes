
import matplotlib.pyplot as plt

def viz(FitnessAccount):

    plt.plot(range(len(FitnessAccount)),[(float(each[0])/float(FitnessAccount[0][0]) - 1.0) * 100.0 for each in FitnessAccount],label = 'Clustering')
    plt.plot(range(len(FitnessAccount)),[(float(each[1])/float(FitnessAccount[0][1]) - 1.0) * 100.0 for each in FitnessAccount],label = 'Efficiency')
    plt.plot(range(len(FitnessAccount)),[(float(each[2])/float(FitnessAccount[0][2]) - 1.0) * 100.0 for each in FitnessAccount],label = 'Density')
    plt.legend()

    plt.xlabel('Number of generations')
    plt.ylabel('Percentage change in fitness')
    plt.show()


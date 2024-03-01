import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def heatmap(matrix, solution = None):

    """
    Plots the heatmap
    :param matrix: matrix containing the active constraints for each solution
    :param solution: plots the solution point if needed
    :return:
    """

    #reshape the array of active constraints in correct order
    array= np.array(matrix)
    dimension = int(np.sqrt(len(matrix)))
    heatmap_matrix = []
    i=0
    while i < dimension**2:
        row=[]
        for j in range(dimension):
            row.append(array[i])
            i = i+1
        heatmap_matrix.append(row)

    #required since the points are reversed row-wise
    heatmap_matrix = np.flip(heatmap_matrix, axis= 0)

    #plot heatmap
    heatmap_matrix = pd.DataFrame(heatmap_matrix)
    fig,ax = plt.subplots(1)
    sns.heatmap(heatmap_matrix, vmin=0, vmax=1, annot= True)
    labels = np.around(np.linspace(0,1,10), decimals=2)
    ax.set_xticks(labels*dimension)
    ax.set_xticklabels(labels)
    ax.set_yticks(labels*dimension)
    ax.set_yticklabels(np.flip(labels))

    #optimal solution
    if solution is not None:
        ax.plot([solution[0]*dimension], [(1 - solution[1]) * dimension], marker="o", markersize=10,
                markeredgecolor="red", markerfacecolor="green")

    plt.show()


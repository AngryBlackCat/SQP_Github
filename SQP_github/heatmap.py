import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from solver import Solver

def heatmap(matrix, solution = None):
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

    heatmap_matrix = np.flip(heatmap_matrix, axis= 0) #required since the points are reversed row-wise

    #plot heatmap
    heatmap_matrix = pd.DataFrame(heatmap_matrix)
    print(heatmap_matrix)

    fig,ax = plt.subplots(1)

    yticks = np.around(np.linspace(0,1,dimension), decimals=2)
    sns.heatmap(heatmap_matrix, xticklabels= yticks,
                yticklabels= np.flip(yticks), vmin=0, vmax=1)
    if solution is not None:
        ax.plot([solution[0]], [dimension - solution[1]], marker="o", markersize=10,
                markeredgecolor="red", markerfacecolor="green")

    plt.show()


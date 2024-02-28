import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def heatmap(matrix, OP_active_constraint):
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

    heatmap_matrix = (np.array(heatmap_matrix) == OP_active_constraint)*1
    heatmap_matrix = np.flip(heatmap_matrix, axis= 0) #required since the points are reversed row-wise

    #plot heatmap
    heatmap_matrix = pd.DataFrame(heatmap_matrix)
    print(heatmap_matrix)
    labels = [0, 1.0]
    sns.heatmap(heatmap_matrix, xticklabels= labels,
                yticklabels= labels, vmin=0, vmax=1)

    plt.show()


import torch
import numpy as np

"""
USELESS CODE
list= []
for i, val in enumerate(x1_obj):
    x1 =val[0]*np.ones((x1_obj.shape[0],1))
    list.append(np.concatenate((x1, x2_obj), axis= 1))

matrix = np.array(list)
"""

def original_problem():

    c = np.array([-5.0, -1.0]).reshape(2,1)
    Q = np.array([[4.0, 2.0],
                 [-1.0, 2.0]])

    A= np.array([[3.0, 0.75],
                [-0.5, 1.0]])
    b = np.matrix([2.5, 0.6]).reshape(2,1)
    return c, Q, A, b

def generate_sample(n_points = 10):
    """
    Generate domain_obj, u_obj, domain_constr
    """
    # Interior points for the objective function
    x1_obj, x2_obj = (np.linspace(start=0, stop= 1, num= n_points).reshape(n_points,1),
                          np.linspace(start=0, stop= 1, num= n_points).reshape(n_points,1))
    list= []
    for i in range(n_points):
        for j in range(n_points):
            list.append([x1_obj[j], x2_obj[i]])

    array= np.array(list)
    matrix = array.reshape(array.shape[0], array.shape[1])

    return matrix



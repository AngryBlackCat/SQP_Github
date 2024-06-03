import numpy as np


def original_problem():
    """
    Defines the problem parameter, then it creates a quadratic problem of the form

    min 1/2x^TQx + c^Tx
    s.t. Ax <= b

    :return:
    """
    c = np.array([-5.0, -1.0]).reshape(2, 1)
    Q = np.array([[9.0, -3.0],
                 [-3.0, 9.0]])

#   q = np.array([[1.0, 0.0],
#                 [0.0, 1.0]])

    A = np.array([[3.0, 1.0],
                 [-0.5, 1.0],
                 [0.0, 1.0]])
    b = np.matrix([2.5, 0.7, 0.8])
    b = b.reshape(b.size, 1)
    return c, Q, A, b


def generate_sample(n_points= 10):

    """
    Generate domain_obj, u_obj, domain_constr

    param: n_points: number of points in which x1 and x2 axes are going to be discretized
    """

    # Interior points for the objective function
    x1_obj, x2_obj = (np.linspace(start=0, stop=1, num=n_points).reshape(n_points, 1),
                          np.linspace(start=0, stop=1, num=n_points).reshape(n_points, 1))
    list = []
    for i in range(n_points):
        for j in range(n_points):
            list.append([x1_obj[j], x2_obj[i]])

    array = np.array(list)
    matrix = array.reshape(array.shape[0], array.shape[1])

    return matrix



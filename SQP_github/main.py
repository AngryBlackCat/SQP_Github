# This is a sample Python script.
#Christian
from det_setting import deterministic, stochastic

'''
        Python code in which the problem and the solver are called
        Solver algorithm: solver.py
        Problem: problem.py
        Heatmap generator: heatmap.py
        Settings (deterministic, stochastic): det_setting.py
'''

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    n_points = 8
    deterministic(n_points)

    n_replicas = 10
    white_noise_variance = 4
    stochastic(n_points, n_replicas, variance=white_noise_variance)









# See PyCharm help at https://www.jetbrains.com/help/pycharm/

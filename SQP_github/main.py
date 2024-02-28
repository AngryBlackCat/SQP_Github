# This is a sample Python script.
#Christian

from problem import *
from heatmap import *
from solver import *
import time
from tempfile import TemporaryFile
from numpy import save
r'''
        Python code in which the problem and the solver are called
        Solver : solver.py
        Problem _ problem.py
'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    n_points = 4

    # We solve the original problem and find out the active constraints
    c, Q, A, b = original_problem()
    problem = Solver(c, Q, A, b)
    model = problem.build_model()
    problem.solve(model, plot_results= True)
    OP_active_constraints = problem.active_constraints
    print("OP active_constraints:", OP_active_constraints)

    #generate the samples
    samples = generate_sample(n_points= n_points)
    AC_matrix = []
    for i in range(len(samples)):
        new_model = problem.build_model(samples[i], index= i)
        problem.solve(new_model, plot_results= True)
        print(f"active_constraints_{i}-th point:", problem.active_constraints)
        AC_matrix.append(problem.active_constraints)
        time.sleep(2)

    save("data.npy", AC_matrix)
    heatmap(AC_matrix, OP_active_constraints)








# See PyCharm help at https://www.jetbrains.com/help/pycharm/

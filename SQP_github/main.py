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

def deterministic(n_points):

    # We solve the original problem and find out the active constraints
    c, Q, A, b = original_problem()
    problem = Solver(c, Q, A, b)
    model = problem.build_model()
    problem.solve(model, plot_results=True)
    optimal_solution = problem.optimal_solution
    OP_active_constraints = problem.active_constraints
    print("OP active_constraints:", OP_active_constraints)

    #generate the samples
    samples = generate_sample(n_points= n_points)
    AC_matrix = []
    for i in range(len(samples)):
        new_model = problem.build_model(samples[i], index= i)
        problem.solve(new_model, plot_results= False)
        print(f"active_constraints_{i}-th point:", problem.active_constraints)
        AC_matrix.append((problem.active_constraints == OP_active_constraints)*1)
        time.sleep(2)

    heatmap(AC_matrix)

def stochastic(n_points, n_replicas, white_noise_variance = 0.5):
    c, Q, A, b = original_problem()
    problem = Solver(c, Q, A, b)
    model = problem.build_model()
    problem.solve(model, plot_results=True)
    optimal_solution = problem.optimal_solution
    OP_active_constraints = problem.active_constraints
    print("OP active_constraints:", OP_active_constraints)

    # generate the samples
    samples = generate_sample(n_points=n_points)
    AC_matrix = []
    for i in range(len(samples)):

        #for each sample, we generate the ratio of correct AC
        correct_ac_count= 0
        for k in range(n_replicas):

            # generate white noise and stochastic c
            white_noise = np.random.normal(0, white_noise_variance, size=(2,1))
            c_tilde = c + white_noise

            #for each element of c_tilde we compute the number of active constraints
            #if AC == OP_ac we increase the correct_ac_count
            new_problem = Solver(c_tilde, Q, A, b)
            new_model = new_problem.build_model(samples[i], index=i)
            new_problem.solve(new_model, plot_results=False)
            print(f"active_constraints_{i}-th point, {k}-th replica:",
                  new_problem.active_constraints)
            if new_problem.active_constraints == OP_active_constraints:
                correct_ac_count = correct_ac_count + 1
            time.sleep(2)

        ratio = correct_ac_count / n_replicas
        print(f"ratio {i}-th point:", ratio)
        AC_matrix.append(ratio)

    print(AC_matrix)
    heatmap(AC_matrix)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    n_points = 5
    n_replicas = 8
    white_noise_variance = 5
    #deterministic(n_points)
    stochastic(n_points, n_replicas)









# See PyCharm help at https://www.jetbrains.com/help/pycharm/

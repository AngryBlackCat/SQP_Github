from heatmap import *
from solver import *

def optimal_solution_AC():

    """
    Build the main quadratic problem, it solves it and provides the optimal solution
    and number of active constraints at that solution
    :return:
    """

    c, Q, A, b = original_problem()
    problem = Solver(c, Q, A, b)
    model = problem.build_model()
    problem.solve(model, plot_results=True)
    optimal_solution = problem.optimal_solution
    OP_active_constraints = problem.active_constraints
    print("OP active_constraints:", OP_active_constraints)

    return OP_active_constraints, optimal_solution

def deterministic(n_points):

    """
    Solves the original problem and then returns the active constraints matrix
    in deterministic settings
    :param n_points: number of points in which each axis is divided
    :return:
    """

    # We solve the original problem and find out the active constraints
    OP_active_constraints, optimal_solution = optimal_solution_AC()

    # generate the samples
    samples = generate_sample(n_points=n_points)
    AC_matrix = []

    #we start solving the problem for each point
    c, Q, A, b = original_problem()
    problem = Solver(c, Q, A, b)
    #print(optimal_solution)
    #new_model = problem.build_model(generated_sample=np.array(optimal_solution), index=0)
    #problem.solve(new_model, plot_results=True)
    #print(f"active_constraints_{0}-th point:", problem.active_constraints)
    #AC_matrix.append((problem.active_constraints == OP_active_constraints) * 1)

    for i in range(len(samples)):
        new_model = problem.build_model(samples[i], index=i)
        problem.solve(new_model, plot_results=False)
        print(f"active_constraints_{i}-th point:", problem.active_constraints)
        AC_matrix.append((problem.active_constraints == OP_active_constraints) * 1)

    #prints the heatmap
    heatmap(AC_matrix, solution=optimal_solution)


def stochastic(n_points, n_replicas, variance=0.5):

    """
    Solves the original problem and then returns the active constraints matrix
    in stochastic settings
    :param n_points: number of points in which each axis is divided
    :param n_replicas: number of replications for the stochastic parameter c
    :param variance: variance of the white noise added to the c parameter
    :return:
    """

    # We solve the original problem and find out the active constraints
    c, Q, A, b = original_problem()
    OP_active_constraints, optimal_solution = optimal_solution_AC()

    # generate the samples
    samples = generate_sample(n_points=n_points)
    AC_matrix = []
    for i in range(len(samples)):

        # for each sample, we generate the ratio of correct AC
        correct_ac_count = 0
        for k in range(n_replicas):

            # generate white noise and stochastic c
            white_noise = np.random.normal(0, variance, size=(2, 1))
            c_tilde = c + white_noise

            # for each element of c_tilde we compute the number of active constraints
            # if AC == OP_ac we increase the correct_ac_count
            new_problem = Solver(c_tilde, Q, A, b)
            new_model = new_problem.build_model(samples[i], index=i)
            new_problem.solve(new_model, plot_results=False)
            print(f"active_constraints_{i}-th point, {k}-th replica:",
                  new_problem.active_constraints)
            if new_problem.active_constraints == OP_active_constraints:
                correct_ac_count = correct_ac_count + 1

        ratio = correct_ac_count / n_replicas
        print(f"ratio {i}-th point:", ratio)
        AC_matrix.append(ratio)

    #prints heatmap
    heatmap(AC_matrix, solution=optimal_solution)
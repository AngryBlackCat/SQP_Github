'''
Solver of quadratic programming problems

Takes objective function and constraints as input
'''

from gurobipy import *
import numpy as np
from problem import *
import matplotlib.pyplot as plt

np.random.seed(1766526)

class Solver:
    def __init__(self, c, Q, A, b):

        #original problem parameters
        self.c = c
        self.Q = Q
        self.A = A
        self.b = b

        # used in the subproblems
        self.I = np.eye(len(Q))

        #initilize parameters
        self.sample = None
        self.active_constraints = 0
        self.index = None
        self.optimal_solution = None

    def plot_domain(self, solution, point_index = None):
        """
        Plot the domain, the constraints and the optimal solution

        :param solution: solution achieved
        :param point_index: x sample index to associate with solution
        :return:
        """
        fig, ax = plt.subplots(1)

        # [0,1] x [0,1] box
        point1 = [1.0, 0.0]
        point2 = [1.0, 1.0]
        point3= [0.0,1.0]
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        ax.plot(x_values, y_values, color= "black", linestyle="-")
        x1_values = [point3[0], point2[0]]
        y1_values = [point3[1], point2[1]]
        ax.plot(x1_values, y1_values, color= "black", linestyle="-")

        # solution point
        ax.plot([solution[0]], [solution[1]], marker="o", markersize=10,
                 markeredgecolor="red", markerfacecolor="green")

        # constraints
        x0 = np.linspace(0.0,1.0, 10)
        cons_list = []
        for k in range(len(self.b)):
            right_hand_side = (self.b[k] - self.A[k, 0] * x0)/self.A[k, 1]
            cons_list.append(right_hand_side)

        tuple_cons=[]
        for cons in cons_list:
            ax.plot(x0, cons.A1, color="blue", linestyle="--")
            tuple_cons.append(cons.A1)

        #fill domain
        tuple_cons = np.column_stack(tuple(tuple_cons))
        ax.fill_between(x0, np.minimum(np.min(tuple_cons, axis=1), 1.0))
        if point_index is None:
            ax.set_title("Domain // original problem")
        else:
            ax.set_title(f"Domain // {point_index}-th point")

        #set domain labels
        ax.set_xlabel("$x_{1}$")
        ax.set_ylabel("$x_{2}$")
        ax.set_xlim([0.0, 1.1])
        ax.set_ylim([0.0, 1.1])
        fig.show()

    def build_model(self, generated_sample = None, index = None):

        """
        We build the original quadratic problem

        :param generated_sample: x sample given
        :param index: x sample index for plot
        :return: optimization model
        """

        if generated_sample is None:
            opt_model = Model(name='quadratic programming problem')

            # variables
            x = opt_model.addMVar((2, 1), vtype=GRB.CONTINUOUS, name='x')
            opt_model.update()

            # objective function
            z = quicksum(x.transpose() @ self.Q)
            xqx = quicksum([z[i] * x[i] for i in range(z.shape[0])])
            obj_fun = quicksum(self.c * x) + 0.5 * xqx
            opt_model.setObjective(obj_fun, GRB.MINIMIZE)

            # constraints
            left_side = self.A @ x
            opt_model.addConstrs((left_side[i].sum() - self.b[i] <= 0.0 for i in range(left_side.shape[0])))
            opt_model.addConstrs(-x[i] <= 0 for i in range(x.shape[0]))
            opt_model.addConstrs(x[i] -1 <= 0 for i in range(x.shape[0]))
            opt_model.update()

        #we build the subproblem, given a specific sample
        else:
            opt_model = Model(name='quadratic programming problem')
            self.index = index

            #introduce generated sample
            self.sample = generated_sample.reshape(generated_sample.shape[0], 1)
            x= self.sample

            # variables
            d = opt_model.addMVar((2, 1), lb= -1000000000,
                                  vtype=GRB.CONTINUOUS, name='d')
            opt_model.update()


            #new objective function
            z= quicksum(d.transpose() @ self.I)
            dqd = quicksum([z[i] * d[i] for i in range(d.shape[0])])
            obj_fun = quicksum((self.c + self.Q @ x) * d) + 0.5 * dqd
            opt_model.setObjective(obj_fun, GRB.MINIMIZE)

            # constraints
            left_side = self.A @ d
            right_side = self.A @ x
            opt_model.addConstrs((left_side[i].sum() <= (self.b[i] - right_side[i])
                                  for i in range(left_side.shape[0])))
            opt_model.addConstrs(d[i] >= -x[i] for i in range(x.shape[0]))
            opt_model.addConstrs(d[i] <= 1-x[i] for i in range(x.shape[0]))
            opt_model.update()

        opt_model.Params.LogToConsole = 0
        return opt_model

    def solve(self, opt_model, plot_results=False):
        """
        We solve the given problem
        :param opt_model: optimization model to be solved
        :param plot_results: True if we want to plot the results, False otherwise
        :return:
        """
        opt_model.optimize()

        #we compute the number of active constraints at solution
        #problem is solved
        if opt_model.SolCount >= 1:
            active_constraints = 0
            for c in opt_model.getConstrs():
                LHS = opt_model.getRow(c).getValue()
                if np.linalg.norm(LHS - c.RHS) < 1e-4:
                    active_constraints = active_constraints + 1
            self.active_constraints = active_constraints

            #plot results if needed
            if plot_results is True:
                var_list = []
                if self.sample is None:
                    for var in opt_model.getVars():
                        var_list.append(var.X)
                    self.optimal_solution = var_list
                    #print("optimal_solution:", self.optimal_solution)
                else:
                    for i, var in enumerate(opt_model.getVars()):
                        print("d:", var.X)
                        print("current x_k:", self.sample.reshape(-1)[i])
                        var_list.append(var.X + self.sample.reshape(-1)[i])
                        print("sum:", var.X + self.sample.reshape(-1)[i])
#                       print("----------------------------------------")
                self.plot_domain(var_list, point_index= self.index)

        #problem is not solved
        else:
            self.active_constraints = 100000
            #print("No feasible solution available")

        opt_model.reset()
        return





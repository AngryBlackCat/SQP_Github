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
        self.c = c
        self.Q = Q
        self.A = A
        self.b = b
        self.I = np.eye(len(Q))
        self.sample = None
        self.active_constraints = 0
        self.index = None
        self.optimal_solution = None

    def plot_domain(self, solution, point_index = None):
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
        ax.plot(x0, cons_list[0].A1, color = "blue", linestyle= "--")
        ax.plot(x0, cons_list[1].A1, color="blue", linestyle="--")

        #fill domain
        ax.fill_between(x0, np.minimum(cons_list[0].A1, cons_list[1].A1))
        if point_index is None:
            ax.set_title("Domain // original problem")
        else:
            ax.set_title(f"Domain // {point_index}-th point")

        ax.set_xlabel("$x_{1}$")
        ax.set_ylabel("$x_{2}$")
        ax.set_xlim([0.0, 1.1])
        ax.set_ylim([0.0, 1.1])
        fig.show()

    def build_model(self, generated_sample = None, index = None):

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

        else:
            opt_model = Model(name='quadratic programming problem')
            self.index = index

            #introduce generated sample
            self.sample = generated_sample.reshape(generated_sample.shape[0], 1)
            x= self.sample
            # variables
            d = opt_model.addMVar((2, 1), vtype=GRB.CONTINUOUS, name='d')
            opt_model.update()
            new_x = x+d

            # objective function (we use the identity matrix instead of Q)
            z = [quicksum(new_x[i]*self.I[i]) for i in range(x.shape[0])]
            new_xqx = quicksum([z[i] * new_x[i] for i in range(len(z))])
            obj_fun = quicksum(self.c * new_x) + 0.5 * new_xqx
            opt_model.setObjective(obj_fun, GRB.MINIMIZE)

            # constraints
            left_side = self.A @ new_x
            opt_model.addConstrs((left_side[i].sum() <= self.b[i] for i in range(left_side.shape[0])))
            opt_model.addConstrs(new_x[i] >= 0 for i in range(x.shape[0]))
            opt_model.addConstrs(new_x[i] <= 1 for i in range(x.shape[0]))
            opt_model.update()

        opt_model.Params.LogToConsole = 0
        return opt_model

    def solve(self, opt_model, plot_results=False):
        opt_model.optimize()

        if opt_model.SolCount >= 1:
            active_constraints = 0
            for c in opt_model.getConstrs():
                LHS = opt_model.getRow(c).getValue()
                if np.linalg.norm(LHS - c.RHS) < 1e-4:
                    active_constraints = active_constraints + 1

            self.active_constraints = active_constraints

            if plot_results is True:
                var_list = []
                if self.sample is None:
                    for var in opt_model.getVars():
                        var_list.append(var.X)
                    self.optimal_solution = var_list
                else:
                    for i, var in enumerate(opt_model.getVars()):
                        var_list.append(var.X + self.sample.reshape(-1)[i])

                self.plot_domain(var_list, point_index= self.index)
        else:
            self.active_constraints = 100000
            #print("No feasible solution available")

        return





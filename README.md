# The role of active constraints on the convergence of stochastic uncostrained algorithms
### Python (Skip if Python3 (>=3.12) is already installed) and a Gurobi license are required

The code calls the Gurobi solver and creates a bi-dimensional Quadratic Programming problem within a [0,1]x[0,1] box. 
The objective function and the constraints of the problem can be manually set by the user in 'problem.py'.

First, the solver finds the optimal solution in the entire feasible set.

Second, given a starting point, the solver finds the 'optimal direction', i.e. the direction that
leads toward the optimal solution from that initial point.

This step is repeated for every point of a grid which discretization is defined by the user. Each optimal direction 
leads to a endpoint, where the number of active constraints are evaluated. 

Therefore, we are exploiting the connection 
starting point -> optimal direction -> endpoint

Finally, the meshgrid of the [0,1]x[0,1] discretized box is plotted. At the center of each sub-square, lies a starting point.
Each square is labeled 1 if the number of active constraints for each endpoint is compared with the number of active constraints at the optimal solution. 

If you need to create a new Python environment and install Python 3.12 with conda, you can use the following command:
```
conda create -n myenv python=3.12
```
Once the environment is created, use:
```
conda activate myenv
```
to activate the Python environment.

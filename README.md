# A Sequential Quadratic Programming algorithm applied on a deterministic and stochastic setting
### Python (Skip if Python3 (>=3.12) is already installed) and a Gurobi license are required

The code calls the Gurobi solver and creates a bi-dimensional Convex Quadratic Programming problem witch specified parameters.
The aim is to assess if the number of active constraints can be useful to understand the quality of an optimal solution
in a stochastic setting.
First, the solver finds the optimal solution.

Second, given an initial point, the solver finds the 'optimal direction', i.e. the direction that
leads toward the optimal solution from that initial point.
This step is repeated for every point of a grid which discretization is defined by the user. Each optimal direction 
leads to a endpoint, where the number of active constraints are evaluated. Then, the number of active constraints 
for each endpoint are compared with the number of active constraints at the optimal solution, and a meshgrid 
is plotted, printing 1 if the comparison is successful (the values are equal), 0 otherwise.

If you need to create a new Python environment and install Python 3.12 with conda, you can use the following command:
```
conda create -n myenv python=3.12
```
Once the environment is created, use:
```
conda activate myenv
```
to activate the Python environment.

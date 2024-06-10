# The role of active constraints on the convergence of stochastic uncostrained algorithms
### Python (Skip if Python3 (>=3.12) is already installed) and a Gurobi license are required

Please read the "Problem settings" PDF file before this ReadMe.

The first experiment involves a Quadratic Programming problem with deterministic parameters.

The code calls the Gurobi solver and creates a bi-dimensional Quadratic Programming problem defined within a [0,1] x [0,1] box. 
The objective function and the constraints of the problem can be manually set by the user in 'problem.py'.

At first, the solver finds the optimal solution in the whole feasible set.

Second, the [0,1] x [0,1] box is discretized in a meshgrid. The level of discretization can be manually defined by the user. 
Given a starting point picked at the center of each sub-square, 
the solver finds the 'optimal direction', i.e. the direction that starts from the starting point and
leads towards an optimal solution.

This step is repeated for every point of the grid. Each optimal direction 
leads to an endpoint, where the number of active constraints are evaluated. 

Therefore, we are exploiting the connection:
sub-square -> starting point -> optimal direction -> endpoint.

Finally, the meshgrid of the [0,1] x [0,1] discretized box is plotted.
Each sub-square is labeled 1 if the number of active constraints is correctly computed (i.e. the number of active constraints of the associated endpoint is equal to the number 
of active constraints at the optimal solution), 0 otherwise.

The second experiment replicates the first one, but it involves a Quadratic Programming problem with a stochastic parameter. 

A white noise is added to the "c" parameter. The number of realizations can be manually defined by the user.
In each sub-square of the final meshgrid, the code prints the ratio between the number of realizations in which the number of active constraints is correctly computed and the total number of realizations.

If you need to create a new Python environment and install Python 3.12 with conda, you can use the following command:
```
conda create -n myenv python=3.12
```
Once the environment is created, use:
```
conda activate myenv
```
to activate the Python environment.

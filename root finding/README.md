_________________________________________________________________
# Root finding with GA
_________________________________________________________________

* Finds root of a function f(x) using fitness function as f(x)^2
* need to specify the expected range of the root as `(x_l,x_u)`
* there are some tunable hyperparameters 
> ppl_size :: polulation size

> generations :: number of generations 

> c_rate :: number of crossover to do 

> m_rate :: number of mutations to do 

> s_prop :: proportion of top performers to be select to go in next generation and reproduce

__________________________________________________________________
### Future updates
__________________________________________________________________

* Different methods for selection, crossover, mutation
* Graphical representation for the evolution of population
* Improved stability at some edge cases
* Allowing for multiple roots by `sharing and neachng`
* Multivariable function.

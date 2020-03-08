_________________________________________________________________
# Root finding with GA
_________________________________________________________________

* Finds root of a function f(x) using fitness function as f(x)^2
* need to specify the expected range of the root as `(x_l,x_u)`
* there are some tunable hyperparameters 
> ppl_size :: polulation size \n
> generations :: number of generations \n
> c_rate :: number of crossover to do \n
> m_rate :: number of mutations to do \n
> s_prop :: proportion of top performers to be select to go in next generation and reproduce \n

__________________________________________________________________
### Future updates
__________________________________________________________________

* Different methods for selection, crossover, mutation
* Graphical representation for the evolution of population
* Improved stability at some edge cases
* Allowing for multiple roots by `sharing and neachng`
* Multivariable function.

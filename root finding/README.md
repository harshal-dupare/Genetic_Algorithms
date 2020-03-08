_________________________________________________________________
# Root finding with GA
_________________________________________________________________

* finds root of a function `f(x)` 
* uses ranking function as `f(x)^2` (closer to `0` => better the rank in sorting => higher the fitness)
* need to specify the expected range of the root as `(x_l,x_u)`
* there are some tunable hyperparameters 
> ppl_size :: population size

> generations :: number of generations 

> c_rate :: number of crossover / ppl_size

> m_rate :: number of mutations / ppl_size

> s_prop :: proportion of population select to go in next generation and reproduce

__________________________________________________________________
### Future updates
__________________________________________________________________

* Different methods for selection, crossover, mutation
* Graphical representation for the evolution of population
* Improved stability at some edge cases
* Allowing for multiple roots by `sharing and neachng`
* Multivariable function

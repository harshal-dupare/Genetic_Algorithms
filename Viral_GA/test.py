from architecture.model_definition import hyper_parameters, parameters,  model_parameters
from problem_space.decision_space import problem_range
import numpy as np
from solution.population import Population, Triggers
import time

params = parameters(ppl_size=10, use_stats=True, generations=10, child_set_size=5, crossover_set_size=30)
hparams = hyper_parameters(lamb = 0.7, step_epsilon = 1e-3, grad_epsilon = 1e-3)
problem = problem_range(decision_dim=3, objective_dim=4, 
			decision_domain={'min':np.full(3,0),'max':np.full(3,1)}, 
			objective_domain={'min':np.full(4,0),'max':np.full(4,1)}, 
			decision_grad_domain={'min':np.full(3,-1000),'max':np.full(3,1000)})
model = model_parameters(params, hparams,problem=problem)

#print("Running the model with \n"+model.__repr__())

PPL = Population(model, use_fitness=False, initial_parameter_stats = None, child_parameter_stats = None, crossover_parameter_stats = None)
PPL.generate_child()
#print(PPL)

PPL.set_stats()

filename = "viralGA_results"+str(int(time.time()))+".txt"
f = open(filename,"w+")

f.write("model parameters : \n")
f.write(model.__repr__())

f.write(PPL.__repr__())

f.close()
#f.write(PPL.stats.___repr__())

from architecture.model_definition import hyper_parameters, parameters,  model_parameters
from problem_space.decision_space import problem_range
import numpy as np
from solution.population import Population, Triggers
import time

params = parameters(ppl_size=20, use_stats=True, generations=10, child_set_size=1, crossover_set_size=30)
hparams = hyper_parameters(lamb = 0.7, step_epsilon = 1e-3, grad_epsilon = 1e-3)
problem = problem_range(decision_dim=3, objective_dim=4, 
			decision_domain={'min':np.full(3,0),'max':np.full(3,1)}, 
			objective_domain={'min':np.full(4,0),'max':np.full(4,1)}, 
			decision_grad_domain={'min':np.full(3,-1000),'max':np.full(3,1000)})
model = model_parameters(params, hparams,problem=problem)

## to check if new compare can be passed
def compare(v1,v2):
	count = 0 
	n =  len(v1.var_objective)
	for i in range(len(v1.var_objective)):
		if v1.var_objective[i] >= v2.var_objective[i]:
			count +=1

	if count > (n/2):
		return -1
	if count == (n/2):
		return 0
	return 1

#print("Running the model with \n"+model.__repr__())

PPL = Population(model, use_fitness=False, initial_parameter_stats = None, child_parameter_stats = None, crossover_parameter_stats = None,compare=compare)
PPL.generate_child(2)
PPL.generate_crossover()
#print(PPL)

PPL.set_stats()
trigger = Triggers(PPL)

filename = "viralGA_results"+str(int(time.time()))+".txt"
f = open(filename,"w+")

f.write("model parameters : \n")
f.write(model.__repr__())

f.write(PPL.__repr__())

PPL.selection(trigger)
PPL.generate_child(2)
PPL.generate_crossover()
PPL.update_ppl_stats()
PPL.update_child_stats()
PPL.update_crossover_stats()

f.write("after selection\n")
f.write(PPL.__repr__())
"""f.write("sorted\n")
PPL.ppl=PPL.sorting(PPL.ppl)
f.write(PPL.__repr__())
"""

f.close()

import time
import numpy as np
import functools
from solution.population import Population, Triggers
from problem_space.decision_space import problem_range
from architecture.model_definition import hyper_parameters, parameters,  model_parameters


###############################
##       INITILIZATION       ##
###############################


## parameteres 
params = parameters(ppl_size=100, use_stats=False, generations=10, child_set_size=5, crossover_set_size=30)
hparams = hyper_parameters(lamb = 0.7, step_epsilon = 1e-3, grad_epsilon = 1e-3)
problem = problem_range(decision_dim=3, objective_dim=4, 
			decision_domain={'min':np.full(3,0),'max':np.full(3,1)}, 
			objective_domain={'min':np.full(4,0),'max':np.full(4,1)}, 
			decision_grad_domain={'min':np.full(3,-1000),'max':np.full(3,1000)})

model = model_parameters(params, hparams,problem=problem)

print("Running the model with \n"+model.__repr__())

PPL = Population(model, problem, use_fitness=False, initial_parameter_stats = None, child_parameter_stats = None, crossover_parameter_stats = None)

PPL.set_stats()
trigger = Triggers(PPL)


###############################
##       INITILIZATION       ##
###############################



###############################
##         MAIN LOOP         ##
###############################


for i in range(params.generations):

	PPL.generate_child(2)
	PPL.update_child_stats()

	PPL.generate_crossover()
	PPL.update_crossover_stats()

	trigger.update(PPL)

	PPL.mutation(trigger)

	PPL.calculat_fitness()

	PPL.selection(trigger)

	PPL.update_ppl_stats()


###############################
##         MAIN LOOP         ##
###############################



#####################################
##         STORING RESULTS         ##
#####################################


print("Final Generation Reached")
print("These are the statistics of final generation", PPL.stats.___repr__() )

filename = "viralGA_results"+str(int(time.time()))+".txt"
print("writing the results to the file :"+filename)
f = open(filename,"w+")

f.write("model parameters : \n")
f.write(model.as_string())

f.write("population : \n")
for v in PPL.ppl:
	f.write(v.__repr__())

f.write("population  statistics : \n")

f.write(PPL.stats.___repr__())

f.close()
#####################################
##         STORING RESULTS         ##
#####################################
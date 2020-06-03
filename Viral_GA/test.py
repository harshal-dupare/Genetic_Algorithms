from architecture.model_definition import hyper_parameters, parameters,  model_parameters
from problem_space.decision_space import problem_range
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from solution.population import Population, Triggers
import time

params = parameters(ppl_size=80,
					use_stats=True, 
					generations=1000, 
					child_set_size=1, 
					crossover_set_size=30,
					itter_max=2000)
hparams = hyper_parameters(lamb = 0.9,
					step_epsilon = 0.05,
					local_epsilon = 0.085,
					min_distance=0.085,
					grad_epsilon=1e-2)
"""
# TNK
problem = problem_range(decision_dim=2, objective_dim=2, 
					decision_domain={'min':np.full(2,0),'max':np.full(2,np.pi)}, 
					objective_domain={'min':np.full(2,0),'max':np.full(2,np.pi)}, 
					decision_grad_domain={'min':np.full(2,-1000),'max':np.full(2,1000)})
"""

# DED
problem = problem_range(decision_dim=2, objective_dim=2, 
					decision_domain={'min':np.asarray([0.1,0]),'max':np.asarray([1,5])}, 
					objective_domain={'min':np.full(2,0),'max':np.full(2,np.pi)}, 
					decision_grad_domain={'min':np.full(2,-1000),'max':np.full(2,1000)})
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

# random seed
random_seed=4333
np.random.seed(random_seed)

PPL = Population(model,
				use_fitness=False,
				initial_parameter_stats = None, 
				child_parameter_stats = None, 
				crossover_parameter_stats = None)

## below is all plotting methods

fig, ax = plt.subplots()
x, y = [PPL.ppl[i].var_objective[0] for i in range(len(PPL.ppl))] ,[PPL.ppl[i].var_objective[1] for i in range(len(PPL.ppl))]
ax.set_title('Generation = '+ str(0))
sc = ax.scatter(x,y)

## region boundary 
# TNK boundary
"""
TNK_thita=np.pi*0.01*np.arange(0,100)/2
TNK_r = np.sqrt(1+0.1*np.cos(16*TNK_thita))
TNK_x = TNK_r*np.cos(TNK_thita)
TNK_y = TNK_r*np.sin(TNK_thita)
plt.plot(TNK_x, TNK_y)
TNK_circle=plt.Circle((0.5,0.5),np.sqrt(0.5),fill=False)
ax.add_artist(TNK_circle)
plt.xlim(0,np.pi)
plt.ylim(0,np.pi)
"""
## end of TNK

# DEB boyndary
plt.xlim(0,1)
plt.ylim(1,12)

DEB_x1=0.1+(1-0.1)*np.arange(0,501)/500
DEB_y1=(7-9*DEB_x1)/DEB_x1
DEB_y2=(9*DEB_x1/DEB_x1)
DEB_y3=6/DEB_x1
DEB_y4=1/DEB_x1
plt.plot(DEB_x1, DEB_y1)
plt.plot(DEB_x1, DEB_y2)
plt.plot(DEB_x1, DEB_y3)
plt.plot(DEB_x1, DEB_y4)
# DEB boyndary

plt.draw()

#print(PPL)

trigger = Triggers(PPL)

filename = "viralGA_results"+str(int(time.time()))+".txt"
f = open(filename,"w+")

f.write("model parameters : \n")
f.write(model.__repr__())

f.write(PPL.__repr__())

snap_interval=10
for i in range(model.parameters.generations):
	PPL.generate_child(2)
	PPL.generate_crossover()
	PPL.selection(trigger)
	#PPL.vc_selection(trigger)
	#PPL.vc_selection2(trigger)
	#print("size"+str(len(PPL.ppl)))
	if i%snap_interval == 0:
		x, y = [PPL.ppl[i].var_objective[0] for i in range(len(PPL.ppl))] ,[PPL.ppl[i].var_objective[1] for i in range(len(PPL.ppl))]
		sc.set_offsets(np.c_[x,y])
		ax.set_title('Generation = ' +str(i))
		fig.canvas.draw_idle()
		plt.pause(0.1)


f.write("after selection\n")
f.write(PPL.__repr__())
"""f.write("sorted\n")
PPL.ppl=PPL.sorting(PPL.ppl)
f.write(PPL.__repr__())
"""

f.close()

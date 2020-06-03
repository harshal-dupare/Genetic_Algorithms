import numpy as np

##########################
##   MODEL DEFINING     ##
##########################

class hyper_parameters:
	def __init__(self,lamb,local_epsilon,step_epsilon,min_distance,grad_epsilon=1e-2,timeline=None):
		self.lamb = lamb
		self.grad_epsilon = grad_epsilon
		self.step_epsilon = step_epsilon
		self.local_epsilon=local_epsilon
		self.min_distance = min_distance
		self.timeline = timeline
		""" timeline variable is array of size generations decides how 
			the user want the timeline to be lower the value of timeline 
			harsh the environment will be at each time for generation """

	def __repr__(self):
		s="HYPERPARAMETERS  \n"
		s+= "lambda : " + str(self.lamb) + "\n"
		s+= "gradient epsilon : " + str(self.grad_epsilon) + "\n"
		s+= "step epsilon : " + str(self.step_epsilon) + "\n"
		s+= "timeline : " + str(self.timeline) + "\n\n"
		return s
 
class parameters:
	def __init__(self,ppl_size,use_stats, generations, child_set_size,crossover_set_size,itter_max=100):
		self.ppl_size = ppl_size
		self.use_stats = use_stats 
		self.generations = generations
		self.child_set_size = child_set_size
		self.crossover_set_size = crossover_set_size
		self.itter_max=itter_max

	def __repr__(self):
		s="PARAMETERS  \n"
		s+= "population size : " + str(self.ppl_size) + "\n"
		s+= "statistics used : " + str(self.use_stats) + "\n"
		s+= "generations : " + str(self.generations) + "\n"
		s+= "child set size : " + str(self.child_set_size) + "\n"
		s+= "crossover set size : " + str(self.crossover_set_size) + "\n\n"
		return s

class model_parameters:
	def __init__(self,parameters,hyper_parameters,problem=None):
		self.parameters = parameters
		self.hyper_parameters = hyper_parameters
		self.problem = problem

	def __repr__(self):
		s=self.hyper_parameters.__repr__()+self.parameters.__repr__()
		return s

##########################
##   MODEL DEFINING     ##
##########################
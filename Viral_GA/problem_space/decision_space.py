import numpy as np


class problem_range:
	## user input
	def __init__(self,decision_dim, objective_dim, decision_domain, objective_domain, decision_grad_domain):
		# int
		self.decision_dim = decision_dim
		self.objective_dim = objective_dim

		# {"min"=[],"max"=[]} 
		# np.arrray is dict
		self.decision_domain = decision_domain
		self.decision_grad_domain = decision_grad_domain
		self.objective_domain = objective_domain

def constrains(var_decision,var_objective,model):
		satisfy = True
		s = np.sum(var_decision)
		if s > 1.5:
			satisfy = False
        ## returns True if all constrains are satisfied False if any is not
        ## need to speify the constrains here
		return satisfy

def random_solution(initial_parameter_stat,model):
	if initial_parameter_stat == None:
		## uniform case
		return model.problem.decision_domain['min']+(model.problem.decision_domain['max']-model.problem.decision_domain['min'])*np.random.rand( model.problem.decision_dim)
	else:
		## user defined way to generate random solution
		pass

def random_gradient(initial_parameter_stat,model):
	if initial_parameter_stat == None:
		## uniform case
		temp = model.problem.decision_grad_domain['min']+(model.problem.decision_grad_domain['max']-model.problem.decision_grad_domain['min'])*np.random.rand( model.problem.decision_dim)
		temp/=np.sqrt(np.sum(temp**2))
		return temp
	else:
		## user defined way to generate random solution
		pass


def crossover_solution(parent1,parent2,crossover_parameter_stat,model):
	xd=(parent1.var_decision+parent2.var_decision)/2
	gd=(parent1.grad_decision +parent2.grad_decision)/2
	gd/=np.sqrt(np.sum(gd**2))
	return xd,gd


def child_solution(parent,child_parameter_stat,model):

	if child_parameter_stat == None:

		shape = parent.var_decision.shape
		u = np.random.uniform(-1,1,shape)                          # uniform random vector
		mod = np.sqrt(np.sum(u**2))                                  # l_2 norm of this vector 
		u/=mod                                                     # converting to unit vector
		r = np.random.rand()                                       # random number from (0,1)
					
		c = parent.var_decision + model.hyper_parameters.step_epsilon*(parent.grad_decision + 2*r*u)
					
					
		u = 2*u*r + parent.grad_decision
		mod = np.sqrt(np.sum(u**2))                                 # l_2 norm of this vector 
		u/=mod                                                     # converting to unit vector       
		u = model.hyper_parameters.lamb*parent.grad_decision + (1-model.hyper_parameters.lamb)*u
		mod =  np.sqrt(np.sum(u**2))                                 # l_2 norm of this vector 
		u/=mod                                                     # converting to unit vector
		
		return c, u

	else:
		## user defined
		pass
	


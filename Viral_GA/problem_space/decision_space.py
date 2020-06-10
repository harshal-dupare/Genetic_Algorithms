import numpy as np


class problem_range:
	## user input
	def __init__(self,decision_dim, objective_dim, decision_domain, objective_domain, decision_grad_domain):
		# int
		self.decision_dim = decision_dim
		self.objective_dim = objective_dim

		# {"min"=[],"max"=[]} 
		# np.arrray in dict
		self.decision_domain = decision_domain
		self.decision_grad_domain = decision_grad_domain
		self.objective_domain = objective_domain

def constrains(var_decision,var_objective,model):
		satisfy = True

		## TNK problem
		"""
		g1 = -var_decision[0]**2-var_decision[1]**2+1+0.1*np.cos(16*np.arctan(var_decision[1]/var_decision[0]))
		g2 = (var_decision[0]-0.5)**2+(var_decision[1]-0.5)**2
		if g1 > 0:
			satisfy = False
			return satisfy
		if g2 > 0.5:
			satisfy = False
			return satisfy
		if var_decision[1] > np.pi:
			satisfy = False
			return satisfy
		if var_decision[1] < 0:
			satisfy = False
			return satisfy
		if var_decision[0] > np.pi:
			satisfy = False
			return satisfy
		if var_decision[0] < 0:
			satisfy = False
			return satisfy
		"""

		#No Hole
		"""
		if var_decision[0] < -1:
			satisfy=False
			return satisfy
		if var_decision[0] > 1:
			satisfy=False
			return satisfy
		if var_decision[1] < 0:
			satisfy=False
			return satisfy
		if var_decision[1] > 4:
			satisfy=False
			return satisfy

		if var_objective[0] < -1:
			satisfy=False
			return satisfy
		if var_objective[0] > 1:
			satisfy=False
			return satisfy
		if var_objective[1] < 0:
			satisfy=False
			return satisfy
		if var_objective[1] > 4:
			satisfy=False
			return satisfy
		"""

		## DEB problem
		
		g1=var_decision[1]+9*var_decision[0]
		g2=-var_decision[1]+9*var_decision[0]
		if g1 < 6:
			satisfy=False
			return satisfy
		if g2 < 1:
			satisfy=False
			return satisfy
		if var_decision[1] > 5:
			satisfy = False
			return satisfy
		if var_decision[1] < 0:
			satisfy = False
			return satisfy
		if var_decision[0] > 1:
			satisfy = False
			return satisfy
		if var_decision[0] < 0.1:
			satisfy = False
			return satisfy
		

		## POL
		"""
		if var_decision[1] > np.pi:
			satisfy = False
			return satisfy
		if var_decision[1] < -np.pi:
			satisfy = False
			return satisfy
		if var_decision[0] > np.pi:
			satisfy = False
			return satisfy
		if var_decision[0] < -np.pi:
			satisfy = False
			return satisfy
		"""

		## Hole Problem
		"""
		if var_decision[1] > 1:
			satisfy = False
			return satisfy
		if var_decision[1] < -1:
			satisfy = False
			return satisfy
		if var_decision[0] > 1:
			satisfy = False
			return satisfy
		if var_decision[0] < -1:
			satisfy = False
			return satisfy
		"""

        ## returns True if all constrains are satisfied False if any is not
		return satisfy

def random_solution(initial_parameter_stat,model):
	if initial_parameter_stat == None:
		## uniform case
		return model.problem.decision_domain['min']+(model.problem.decision_domain['max']-model.problem.decision_domain['min'])*np.random.rand( model.problem.decision_dim)
	else:
		## user defined way to generate random solution basied on init_params_stats
		pass

def random_gradient(initial_parameter_stat,model):
	if initial_parameter_stat == None:
		## uniform case
		temp = np.random.normal(0,1,model.problem.decision_dim)
		temp/=np.sqrt(np.sum(temp**2))
		return temp
	else:
		## user defined way to generate random solution
		pass

def intersection_solver(v1,v2,r1,r2):
	# adding small vaue for stability can remove it if removed all same solution in selection
    d=np.sum((v1-v2)**2)**(1/2)+0.0000000001
    v12=v2-v1+0.0000000001
    r = np.random.normal(0,1,v1.shape[0])
    r= r-(np.dot(v12,r)/np.dot(v12,v12))*v12
    #center x0
    t0=(r1**2-r2**2+d**2)/(2*d**2)
    ## (r1**2 - r2**2 + d**2)/(2*d**2)
    x0=v1+t0*(v2-v1)
    ## setting up at^2+bt+c
    a=np.sum((r)**2)
    b=2*np.dot(r,x0-v1)
    c=np.sum((x0-v1)**2)-r1**2
    
    ## solving for t
    delta = b**2 -4*a*c
    #print(delta)
    t=(-b-delta**(1/2))/(2*a)
    
    ## getting the point on 
    ans = x0+t*(r)
    
    return ans

"""
Maths behind Intersection solver
|v1 - v2| = d
(x-v1)*(x-v1)=r1**2=x*x-2*x*v1+v1*v1
(x-v2)*(x-v2)=r2**2=x*x-2*x*v2+v2*v2

## eq of plane
2x*(v2-v1)=r1**2-r2**2-np.sum(v1**2)+np.sum(v2**2)

x=v1+t(v2-v1)x
2*v1*v2+2*t*d**2-v1**2-v2**2=r2**2-r1**2
t0=(r2**2-r1**2+d**2)/(2d**2) ## t==>x0
## center
x0=v1+t0*(v2-v1)
"""


def crossover_solution(parent1,parent2,crossover_parameter_stat,model):
	d=np.sqrt(np.sum((parent1.var_decision-parent2.var_decision)**2))
	r=model.hyper_parameters.min_distance + (1+np.random.rand())*d/2
	xd=intersection_solver(parent1.var_decision,parent2.var_decision,r,r)

	gd=(parent1.grad_decision +parent2.grad_decision)/2
	gd/=np.sqrt(np.sum(gd**2))

	## spherical intersection

	return xd,gd


def child_solution(parent,child_parameter_stat,model):

	if child_parameter_stat == None:
		shape = parent.var_decision.shape
		u = np.random.normal(0,1,shape)  # an array of d normally distributed random variables
		norm=np.sum(u**2) **(0.5)
		u=u/norm
		r = np.random.rand()**(1.0/shape[0])                              # random number from (0,1) accoring to d*r^(d-1)/R^d distribution

		u=model.hyper_parameters.step_epsilon*parent.grad_decision + model.hyper_parameters.local_epsilon*r*u
					
		c = parent.var_decision + u
					
		mod = np.sqrt(np.sum(u**2))                                 # l_2 norm of this vector 
		u/=mod                                                     # converting to unit vector       
		u = model.hyper_parameters.lamb*parent.grad_decision + (1-model.hyper_parameters.lamb)*u
		mod =  np.sqrt(np.sum(u**2))                                 # l_2 norm of this vector 
		u/=mod                                                     # converting to unit vector
		
		return c, u

	else:
		## user defined
		pass
	


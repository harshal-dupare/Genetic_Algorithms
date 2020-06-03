import numpy as np 
from problem_space import objective_space
from problem_space import decision_space
from problem_space import fitness_space
from problem_space.decision_space import constrains

class virus:

	def __init__(self, model, make_as = "initial", initial_parameter_stats = None, use_fitness=False, child_parameter_stats = None, parent=None, parent1=None, parent2=None, crossover_parameter_stats = None):

		if make_as == "initial":
			# numpy arrays
			self.var_decision = decision_space.random_solution(initial_parameter_stats,model)
			self.var_objective = objective_space.function(self.var_decision,model)
			itter_max = model.parameters.itter_max
		
			## looping until constrains are satisfied
			while not constrains(self.var_decision,self.var_objective,model):
				self.var_decision = decision_space.random_solution(initial_parameter_stats,model)
				self.var_objective = objective_space.function(self.var_decision,model)
				itter_max=-1
				if itter_max < 0:
					break
			#print(itter_max)
			self.dimension = [self.var_decision.shape,self.var_objective.shape]

			self.grad_decision = decision_space.random_gradient(initial_parameter_stats,model)
			self.grad_objective = objective_space.gradient(self.var_decision,self.var_objective,self.grad_decision,model)

			self.set_fitness(use_fitness)

		elif make_as == "child":

			# numpy arrays
			self.var_decision, self.grad_decision  = decision_space.child_solution(parent,child_parameter_stats,model)
			self.var_objective = objective_space.function(self.var_decision,model)
			## looping until constrains are satisfied
			itter_max = model.parameters.itter_max
			
			while not constrains(self.var_decision,self.var_objective,model):
				self.var_decision, self.grad_decision  = decision_space.child_solution(parent,child_parameter_stats,model)
				self.var_objective = objective_space.function(self.var_decision,model)
				itter_max-=1
				if itter_max < 0:
					self.var_decision, self.grad_decision = parent.var_decision, parent.grad_decision
					break
			#print(itter_max)
			self.dimension = [self.var_decision.shape,self.var_objective.shape]

			self.grad_objective = objective_space.gradient(self.var_decision,self.var_objective,self.grad_decision,model)

			self.set_fitness(use_fitness)

		elif make_as == "crossover":

			# numpy arrays
			self.var_decision , self.grad_decision = decision_space.crossover_solution(parent1,parent2,crossover_parameter_stats,model)
			self.var_objective = objective_space.function(self.var_decision,model)
			"""## looping until constrains are satisfied
			while not constrains(self.var_decision,self.var_objective,model):
				self.var_decision = decision_space.crossover_solution(parent1,parent2,crossover_parameter_stats,model)
				self.var_objective = objective_space.function(self.var_decision,model)"""

			self.dimension = [self.var_decision.shape,self.var_objective.shape]

			self.grad_objective = objective_space.gradient(self.var_decision,self.var_objective,self.grad_decision,model)

			self.set_fitness(use_fitness)

		else:
			print("wrong make_as input!")



	def children(self,model,count,child_parameter_stats=None,use_fitness=False):
		children_set = []
		for i in range(count):
			children_set.append(virus(model,make_as="child",use_fitness=use_fitness,child_parameter_stats=child_parameter_stats,parent = self))

		return children_set

	def __repr__(self):
		s = ""
		s+= "decision variable : " + str(self.var_decision) +"\n"
		s+= "decision gradient : " + str(self.grad_decision) +"\n"
		s+= "objective variable : " + str(self.var_objective) +"\n"
		s+= "objective gradient : " + str(self.grad_objective) +"\n"
		s+= "fitness : " + str(self.fitness) +"\n \n"
		return s

	def set_fitness(self,use_fitness=False):

		if use_fitness:
			f = 0
			## user defined fitness
			## returns a scalar value as float/double and a list of fitness for each input parameter i.e. a list of size 4
			## higher the value higher the fitness

			self.fitness = f
		else:
			self.fitness = None

		pass
		


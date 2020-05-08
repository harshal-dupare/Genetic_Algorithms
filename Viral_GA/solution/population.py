import numpy as np 
import scipy
from problem_space import objective_space
from problem_space import decision_space
from problem_space import fitness_space
from solution.virus import virus


###############################
##   STATISTICS DEFINING     ##
###############################

class Stats:
	def __init__(self,use_stats,ppl,ppl_type):
		## code to get required stats
		if use_stats:
			self.used = True
			if ppl != None:
				self.update(ppl)

		else:
			self.used = False
		self.type = ppl_type

	def update(self,ppl):
		if self.used:
			## code to update all stats
			self.size = max(len(ppl),1)
			obj = np.asarray([i.var_objective for i in ppl])
			if obj.shape[0]==len(obj):
				obj_axis = 0
			else:
				 obj_axis = 1
			dec = np.asarray([i.var_decision for i in ppl])
			if dec.shape[0]==len(obj):
				dec_axis = 0
			else:
				 dec_axis = 1
			self.avg_objective = np.mean(obj,axis=obj_axis)
			self.avg_decision = np.mean(dec,axis=dec_axis)
			self.variance_obj = np.var(obj,axis=obj_axis)
			self.variance_dec = np.var(dec,axis=dec_axis)


	def __repr__(self):
		## returns contains of self as string
		if self.used:
			s=self.type+" Stats\n\n"
			s+=self.type+" Population size:"+str(self.size)+"\n"
			s+="objective mean :"+str(self.avg_objective)+"\n"
			s+="objective variance :"+str(self.variance_obj )+"\n"
			s+="decision mean :"+str(self.avg_decision )+"\n"
			s+="decision variance:"+str(self.variance_dec )+"\n"
			s+="\n"
			return s
		else:
			return "Empty"
class Triggers:
	def __init__(self,PPL):
		## "normal" "weak" "strong" "selective"
		self.selection_type = "normal"
		self.mutation_type = "normal"
		## define the triggers
		## initilize them

	def update(self,PPL):
		## process to calculat the triggers
		pass

###############################
##   STATISTICS DEFINING     ##
###############################


class Population:
	def __init__(self, model, use_fitness=False, initial_parameter_stats = None, child_parameter_stats = None, crossover_parameter_stats = None):

		self.model = model

		self.ppl_size = model.parameters.ppl_size
		self.ppl_stats = None

		self.child_set_size = model.parameters.child_set_size
		self.crossover_set_size = model.parameters.crossover_set_size
		self.use_stats = model.parameters.use_stats

		self.use_fitness = use_fitness
		self.initial_parameter_stats = initial_parameter_stats
		self.child_parameter_stats = child_parameter_stats
		self.crossover_parameter_stats = crossover_parameter_stats

		self.child_stats = None
		self.crossover_stats = None

		self.child_set = None
		self.crossover_set = None

		self.generate_population()

	def set_stats(self):
		if self.use_stats:
			self.update_ppl_stats()
			self.update_child_stats()
			self.update_crossover_stats()

	## population
	def generate_population(self):
		temp = []
		for i in range(self.ppl_size):
			temp.append(virus(model=self.model, make_as = "initial", initial_parameter_stats=self.initial_parameter_stats ,use_fitness=self.use_fitness,child_parameter_stats=self.child_parameter_stats))
		self.ppl = temp

	def update_ppl_stats(self):
		if self.use_stats:
			self.ppl_stats = Stats(use_stats=self.use_stats, ppl = self.ppl,ppl_type="Population")
			


	## children
	def generate_child(self):
		PPL_CHILD_SET = []
		for v in self.ppl:
			PPL_CHILD_SET += v.children(self.model,count=self.child_set_size, child_parameter_stats=self.child_parameter_stats, use_fitness=self.use_fitness)
		self.child_set = PPL_CHILD_SET

	def update_child_stats(self):
		if self.use_stats:
			self.child_stats = Stats(use_stats=self.use_stats, ppl = self.child_set,ppl_type="Child")



	## 	Crossover
	def generate_crossover(self):
		pass


	def update_crossover_stats(self):
		if self.use_stats:
			self.crossover_stats = Stats(use_stats=self.use_stats, ppl = self.crossover_set,ppl_type="Crossover")




	def mutation(self,trigger):
		pass


	def calculat_fitness(self):
		for v in self.ppl:
			v.set_fitness(self.use_fitness)
		if self.child_set != None:
			for v in self.child_set:
				v.set_fitness(self.use_fitness)
		if self.crossover_set != None:
			for v in self.crossover_set:
				v.set_fitness(self.use_fitness)


	def selection(self,trigger):
		pass

	
	def compare(self,v1,v2):
		pass

		

	def sorting(self,use_fitness):
		pass

	def __repr__(self):
		s="Population\n\n"
		for v in self.ppl:
			s+=v.__repr__()
		s+="Child Population\n\n"
		if self.child_set != None:
			for v in self.child_set:
				s+=v.__repr__()
		s+="Crossover Population\n\n"
		if self.crossover_set != None:
			for v in self.crossover_set:
				s+=v.__repr__()
		
		if self.ppl_stats.used:
			s+=self.ppl_stats.__repr__()
		if self.child_stats.used:
			s+=self.child_stats.__repr__()
		'''if self.crossover_stats.used:
			s+=self.crossover_stats.__repr__()'''
		return s

import numpy as np 
import scipy
import functools
from problem_space import objective_space
from problem_space import decision_space
from problem_space import fitness_space
from solution.virus import virus
from problem_space.decision_space import constrains
from solution.vertexcover import vertex_cover


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
			self.size=0
			self.avg_objective = 'None'
			self.avg_decision = 'None'
			self.variance_obj = 'None'
			self.variance_dec = 'None'
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
	def __init__(self, model, use_fitness=False, initial_parameter_stats = None, child_parameter_stats = None, crossover_parameter_stats = None,compare=None):

		self.model = model
		self.compare = compare
		self.ppl_size = model.parameters.ppl_size

		self.child_set_size = model.parameters.child_set_size
		self.crossover_set_size = model.parameters.crossover_set_size
		self.use_stats = model.parameters.use_stats

		self.use_fitness = use_fitness
		self.initial_parameter_stats = initial_parameter_stats
		self.child_parameter_stats = child_parameter_stats
		self.crossover_parameter_stats = crossover_parameter_stats

		self.child_set = None
		self.crossover_set = None

		self.generate_population()

	## population
	def generate_population(self):
		temp = []
		n=self.ppl_size
		while n > 0:
			v=virus(model=self.model, make_as = "initial", initial_parameter_stats=self.initial_parameter_stats ,use_fitness=self.use_fitness,child_parameter_stats=self.child_parameter_stats)
			if constrains(v.var_decision,v.var_objective,self.model):
				temp.append(v)
			n-=1
			
		self.ppl = temp
			


	## children
	def generate_child(self,select_size):
		PPL_CHILD_SET = []
		for v in self.ppl:
			PPL_CHILD_SET += self.sorting(v.children(self.model,count=self.child_set_size, child_parameter_stats=self.child_parameter_stats, use_fitness=self.use_fitness))[0:select_size]

		self.child_set = PPL_CHILD_SET

	## 	Crossover
	def generate_crossover(self):
		n=len(self.ppl)
		PPL_crossover_set=[]
		for i in range(self.model.parameters.crossover_set_size):
			r1=np.random.randint(n)
			r2=np.random.randint(n-1)+1
			r2=(r1+r2)%n
			v=virus(model=self.model, make_as = "crossover", use_fitness=self.use_fitness,parent1=self.ppl[r1], parent2 = self.ppl[r2], crossover_parameter_stats = self.crossover_parameter_stats)
			if constrains(v.var_decision,v.var_objective,self.model):
				PPL_crossover_set.append(v)
			
		if len(PPL_crossover_set)>0:
			self.crossover_set=PPL_crossover_set
			#print("printing cs set")
			#for v in self.crossover_set:
				#print(constrains(v.var_decision,v.var_objective,self.model))

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
		## handelig ppl
		## selection sizes baised on trigger
		"""selected_ppl_size=int(0.5*self.ppl_size)
		self.ppl=self.sorting(self.ppl)[0:selected_ppl_size]

		## handeling child set
		## how many to selctet from child set
		selected_child_size=int(0.5*len(self.child_set))
		self.ppl=self.sorting(self.ppl)[0:selected_child_size]"""

		for i in range(len(self.ppl)):
			v=[self.ppl[i]]+self.child_set[i*self.child_set_size:(i+1)*self.child_set_size]
			self.ppl[i]=self.sorting(v)[0]

		## handeling crossover set
		## how many to selctet from crossover set
		if self.crossover_set !=None:
			selected_crossover_size=max(1,int(0.5*len(self.crossover_set)))
			self.crossover_set=self.sorting(self.crossover_set)[0:selected_crossover_size]

		if self.crossover_set !=None:
			self.ppl=self.ppl+self.crossover_set
		if self.child_set != None:
			self.ppl=self.ppl+self.child_set
		self.ppl=self.sorting(self.ppl)[0:self.ppl_size]

	def vc_selection(self,trigger):

		for i in range(len(self.ppl)):
			v=[self.ppl[i]]+self.child_set[i*self.child_set_size:(i+1)*self.child_set_size]
			self.ppl[i]=self.sorting(v)[0]

		tppl=self.ppl+self.crossover_set
		tppl=self.sorting(tppl)
		preserv=int(0.5*self.ppl_size)+1
		vc=vertex_cover(tppl[preserv:],self.model.hyper_parameters.min_distance)
		k=[i in range(len(tppl[preserv:]))]
		vc=list(set(k)-set(vc))
		if len(vc) > 0:
			self.ppl=tppl[0:preserv]
			vc=sorted(vc)
			for b in vc:
				self.ppl.append(tppl[b+preserv])
		
			n= len(self.ppl)
			if n <= self.ppl_size:
				temp = []
				m= self.ppl_size-n
				while m > 0:
					v=virus(model=self.model, make_as = "initial", initial_parameter_stats=self.initial_parameter_stats ,use_fitness=self.use_fitness,child_parameter_stats=self.child_parameter_stats)
					if constrains(v.var_decision,v.var_objective,self.model):
						temp.append(v)
					m-=1
				self.ppl+=temp
			else:
				self.ppl=self.sorting(self.ppl)[0:self.ppl_size]

		else:
			self.generate_population()
			self.ppl[0:preserv]=tppl[0:preserv]

	def vc_selection2(self,trigger):

		for i in range(len(self.ppl)):
			v=[self.ppl[i]]+self.child_set[i*self.child_set_size:(i+1)*self.child_set_size]
			self.ppl[i]=self.sorting(v)[0]

		tppl=self.ppl+self.crossover_set
		tppl=self.sorting(tppl)
		preserv=int(0.5*self.ppl_size)+1
		vc=vertex_cover(tppl,self.model.hyper_parameters.min_distance)
		k=[i in range(len(tppl))]
		vc=list(set(k)-set(vc))
		for b in vc:
			self.ppl.append(tppl[b])


	## Using counting pereto optima
	def defalt_compare(self,v1,v2):
		count = 0 
		n =  len(v1.var_objective)
		for i in range(len(v1.var_objective)):
			if v1.var_objective[i] <= v2.var_objective[i]:
				count +=1

		if count > (n/2):
			return -1
		if count == (n/2):
			return 0
		return 1

	def sorting(self,arr,use_fitness=False):
		if self.compare != None:
			return sorted(arr, key=functools.cmp_to_key(self.compare))
		else:
			return sorted(arr, key=functools.cmp_to_key(self.defalt_compare))

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
		return s

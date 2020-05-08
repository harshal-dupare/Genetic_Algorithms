import numpy as np

def function(var_decision,model):
	## user defined functions
	x0,x1,x2=var_decision[0],var_decision[1],var_decision[2]
	return np.asarray([15*(x0)**2-13*(x1)+(x2)/5,25*(x1)**4-100*(x0)+(x2)/5.5,115*(x1)**2-13*(x2)**3+(x2)/56,1.5*(x2)**2-13*(x1*x0)+(x2)/50])
	##  output a  np.array of specified dim


def gradient(var_decision,var_objective,grad_decision,model):
	return ((function(var_decision+model.hyper_parameters.grad_epsilon*grad_decision,model)-var_objective)/model.hyper_parameters.grad_epsilon)

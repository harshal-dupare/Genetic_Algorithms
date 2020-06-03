import numpy as np

def hole_no_hole(x0,x1,hole=True):
	# function parameters
	q=0.2
	p=2
	d0=0.02

	#hardness
	h=2

	#translation
	delta=1-(1/np.sqrt(2))
	x0_prime = x0 + delta
	x1_prime = x1 + delta

	# rotation of 45 degrees
	alpha = np.pi/4
	x0_2prime=x0_prime*np.cos(alpha)+x1_prime*np.sin(alpha)
	x1_2prime=-x0_prime*np.sin(alpha)+x1_prime*np.cos(alpha)

	# scale of pi
	x0_3prime = np.pi*x0_2prime
	x1_3prime = np.pi*x1_2prime

	# change into problem coordinates
	u = np.sin(x0_3prime/2)
	v = (np.sin(x1_3prime/2))**2

	# apply hardness

	if u >= 0:
		u_prime = u**h
	else:
		u_prime = -1*(-1*u)**h

	v_prime=v**(1/h)

	# problem parameters
	t=u_prime
	a=v_prime*2*p

	# other parameters computation
	if a > p:
		b=0
	else: 
		b=(p-a)*np.exp(q)
	
	if not hole:
		b=0 
	
	d=(q*a/2)+d0
	c=q/(d**2)

	# objective functions for NO HOLE & HOLE PROBLEM
	f1=(t+1)**2 + a + b*np.exp(-1*c*((t-d)**2))
	f2=(t-1)**2 + a + b*np.exp(-1*c*((t+d)**2))

	return f1,f2

def function(var_decision,model):
	## user defined functions
	x0,x1=var_decision[0],var_decision[1]

	## TNK problem
	"""
	f1=x0
	f2=x1
	"""

	## DEB
	
	f1=x0
	f2=(1+x1)/x0

	## POL
	"""
	a=0.5*np.sin(1)-2*np.cos(1)+np.sin(2)-1.5*np.cos(2)
	b=0.5*np.sin(x0)-2*np.cos(x0)+np.sin(x1)-1.5*np.cos(x1)
	c=1.5*np.sin(1)-np.cos(1)+2*np.sin(2)-0.5*np.cos(2)
	d=1.5*np.sin(x0)-np.cos(x0)+2*np.sin(x1)-0.5*np.cos(x1)

	f1=1+(a-b)**2+(c-d)**2
	f2=(x0+3)**2+(x1+1)**2
	"""

	## Hole
	"""
	f1,f2=hole_no_hole(x0,x1,hole=True)
	"""

	## NO Hole
	"""
	f1,f2=hole_no_hole(x0,x1,hole=False)
	"""

	##  output a  np.array of specified dim
	return np.asarray([f1,f2])

def gradient(var_decision,var_objective,grad_decision,model):
	return ((function(var_decision+model.hyper_parameters.grad_epsilon*grad_decision,model)-var_objective)/model.hyper_parameters.grad_epsilon)

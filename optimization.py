from scipy.optimize import minimize
import linalg

def getMatrixConstraints(votes, winner):
	'''
	Return matrix A, s.t Ax >= b where b is the zero vector
	'''
	return [linalg.subtract(votes[winner], votes[candidate]) 
		for candidate in votes.keys() if candidate != winner]

def fixMatrixVariableConstraints(constraint):
	'''
	Turn [-3, 4, -1]*[x0, x1, x2]^T into lambda x: -3x0 + 4x1 - x2
	Used for turning matrix variable constraints into lambda constraints 
	'''
	return lambda x: sum([x[i]*constraint[i] for i in range(len(constraint))]) - 0.1

def fixPositional(i):
	'''
	Fix positional weighting system such that w[n] >= w[n-1]
	'''
	return lambda x: x[i] - x[i+1]

def createLambdaConstraints(A, numCandidates):
	'''
	Turn our matrix constraints into lambda constraints to be input into the slsqp function
	'''
	# create lambda constraints from variable matrix constraints
	constraints = [{'type': 'ineq', 'fun': fixMatrixVariableConstraints(constraint)} 
		for constraint in A]
	# fix w[n] >= w[n-1] 
	i = 0
	while i + 1 < numCandidates:
		constraints.append({'type': 'ineq', 'fun': fixPositional(i)})
		i += 1
	# fix x[0] = n - 1
	constraints.append({'type': 'eq', 'fun': lambda x: x[0] - numCandidates +1})
	return tuple(constraints)

def slsqp(votes, winner, numCandidates):
	'''
	Returns vector that minimizes bordaDistance with constraints cons
	'''
	A = getMatrixConstraints(votes, winner)
	cons = createLambdaConstraints(A, numCandidates)
	# initial guess is the borda
	initial = [i for i in range(numCandidates)][::-1] 
	# minimize bordaDistance given our constraints
	res = minimize(linalg.bordaDistance, initial, method='SLSQP', 
		constraints = cons, options={"disp": False})
	# get new weighting vector
	new_weight = res.x.tolist()
	return [round(e, 2) for e in new_weight]




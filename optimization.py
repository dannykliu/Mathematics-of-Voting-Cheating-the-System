from scipy.optimize import minimize

def distance(x):
	'''
	Returns distance of x to equivalent borda vector
	'''
	n = len(x)
	avgDist = (x[0] + x[-1])/n
	borda = []
	initial = x[0]
	for i in range(n):
		borda.append(initial)
		initial -= avgDist
	funcVal = 0
	for i in range(n):
		funcVal += (x[i] - borda[i])**2

	return funcVal

def subtract(a, b):
	'''
	returns the result of a - b
	'''
	assert(len(a) == len(b))
	result = []
	for i in range(len(a)):
		result.append(a[i] - b[i])

	return result

def getMatrixConstraints(votes, winner):
	mat = []
	# compute variable constraints
	for candidate in votes.keys():
		if candidate != winner:
			mat.append(subtract(votes[winner], votes[candidate]))
	# fix w_n > w_n-1 by adding vectors [1, -1, 0, ..., 0] down to [0, ..., 0, 1, -1]
	# i = 0
	# while i + 1 < len(votes):
	# 	cons = [0]*(len(votes))
	# 	cons[i] = 1
	# 	cons[i+1] = -1
	# 	mat.append(cons)
	# 	i += 1
	#print('CONSTRAINT: ', mat)
	return mat

def getFunc(constraint):
	# subtract 1 to make sure that our winner always wins by at least 1 point
	return lambda x: sum([x[i]*constraint[i] for i in range(len(constraint))]) - 0.1

def getFunc2(i):
	return lambda x: x[i] - x[i+1]

def createLambdaConstraints(A, numCandidates):
	constraints = []
	# create lambda constraints from matrix constraints
	for constraint in A:
		constraints.append({'type': 'ineq', 'fun': getFunc(constraint)})
	# fix w_n > w_n-1 
	i = 0
	while i + 1 < numCandidates:
		constraints.append({'type': 'ineq', 'fun': getFunc2(i)})
		i += 1
	# fix first element = n - 1
	constraints.append({'type': 'eq', 'fun': lambda x: x[0] - numCandidates +1})
	return tuple(constraints)

def sequentialQuadratic(votes, winner, numCandidates):
	A = getMatrixConstraints(votes, winner)
	cons = createLambdaConstraints(A, numCandidates)
	initial = [i for i in range(numCandidates)][::-1] # initial guess is the borda
	res = minimize(distance, initial, method='SLSQP', 
		constraints = cons, options={"disp": False})
	#print(res)
	new_weight = res.x.tolist()
	return [round(e, 2) for e in new_weight] # round off three decimal places

def makeYourCandidateWin(votes, winner, numCandidates):
	return sequentialQuadratic(votes, winner, numCandidates)



'''
Custom linear algebra library
'''

def subtract(a, b):
	'''
	returns the result of a - b for two nx1 vectors
	'''
	assert(len(a) == len(b))
	return [a[i] - b[i] for i in range(len(a))]

def dot(vec1, vec2):
	'''
	returns the result of a.b for two nx1 vectors
	'''
	assert(len(vec1) == len(vec2))
	return sum([vec1[i]*vec2[i] for i in range(len(vec1))])

def bordaDistance(x):
	'''
	Returns squared distance of x to its equivalent borda count vector
	'''
	n = len(x)
	borda = [i for i in range(n)][::-1] # [n-1, n-2, ..., 0]
	return sum([(x[i] - borda[i])**2 for i in range(n)])

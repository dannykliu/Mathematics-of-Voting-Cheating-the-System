import optimization as optimize

def dotProduct(vec1, vec2):
	assert(len(vec1) == len(vec2))
	answer = 0
	for i in range(len(vec1)):
		answer += vec1[i]*vec2[i]
	return answer

def addOnePreference(results, preference, occ):
	assert(set(results.keys()) >= set(list(preference)))
	for i in range(len(preference)): 
		results[preference[i]][i] += occ

def countVotes(candidates, data):
	'''
	Returns number of votes each candidate receives
	'''
	results = {}
	numCandidates = len(candidates)
	for candidate in candidates:
		results[candidate] = [0] * numCandidates
	for preference in data.keys():
		addOnePreference(results, preference, data[preference])
	#print("COUNT VOTES: ", results)
	return results

def computeScores(votes, weighting): 
	scores = {}
	for key in votes.keys():
		scores[key] = round(dotProduct(votes[key], weighting), 2)
	#print("COMPUTE SCORE: ", votes)
	return scores

def subtract(a, b):
	'''
	returns the result of a - b
	'''
	assert(len(a) == len(b))
	result = []
	for i in range(len(a)):
		result.append(a[i] - b[i])
	return result

def findWV(candidates, data, winner):
	initial_weighting = [i for i in range(len(candidates))][::-1] # [n-1, n-2, ..., 0]
	votes = countVotes(candidates, data)
	scores = computeScores(votes, initial_weighting)
	numCandidates = len(candidates)
	systemWinner = max(scores, key=scores.get)
	print("Points each candidate would receive under the Borda count \n" , scores)
	if systemWinner == winner:
		print(winner + " already wins!")
		return
	new_weight = optimize.makeYourCandidateWin(votes, winner, numCandidates)
	print("New weighting weighting such that " + winner + " is the winner \n", new_weight)
	new_scores = computeScores(votes, new_weight)
	print("Points each candidate now receives under the new weighting vector \n", new_scores)


findWV(['A', 'B', 'C'], {'BCA': 4, 'CBA': 10, 'ABC': 1}, 'B')
print("------------------------------")
findWV(['A', 'B', 'C'], {'ABC': 4, 'BCA': 1}, 'B')
print("------------------------------")
findWV(['A', 'B', 'C'], {'ABC': 4, 'BAC': 1}, 'B')




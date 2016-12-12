import optimization as optimize
import linalg

def addOnePreference(results, preference, occ):
	'''
	Adds the preference order of a single voter to the societal preference
	'''
	assert(set(results.keys()) >= set(list(preference)))
	for i in range(len(preference)): 
		results[preference[i]][i] += occ

def countVotes(candidates, data):
	'''
	Returns the number of first, second, ..., nth place votes a candidate receives
	Input: arr, dict[str -> num]
	Output: dict[str -> arr]
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
	'''
	The score a candidate receives is the dot product of the ranked votes he/she received with the weighting vector
	Input: dict[str -> arr], arr
	Output: dict[str -> num]
	'''
	scores = {}
	for key in votes.keys():
		scores[key] = round(linalg.dot(votes[key], weighting), 2)
	return scores

def findWV(candidates, data, winner):
	'''
	Input: 
	list of candidates: ['A', 'B', 'C']
	map of preferences -> occurence: ['BCA': 4, 'CBA': 10, 'ABC': 1]
	who you want to win the election: 'B'
	Output: tuple
	weighting vector w that minimizes ||w-b||^2 and allows the specified winner to win
	score each candidate has
	'''
	initial = [i for i in range(len(candidates))][::-1] 
	votes = countVotes(candidates, data)
	scores = computeScores(votes, initial)
	numCandidates = len(candidates)
	systemWinner = max(scores, key=scores.get)
	if systemWinner == winner:
		return (initial, scores)
	new_weight = optimize.slsqp(votes, winner, numCandidates)
	newScores = computeScores(votes, new_weight)
	return (new_weight, newScores)


print(findWV(['A', 'B', 'C'], {'BCA': 4, 'CBA': 10, 'ABC': 1}, 'B'))
print(findWV(['A', 'B', 'C'], {'ABC': 4, 'BCA': 1}, 'B'))
print(findWV(['A', 'B', 'C'], {'ABC': 4, 'BAC': 1}, 'B'))







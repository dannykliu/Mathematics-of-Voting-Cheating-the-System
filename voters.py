# candidates {0, 1, ..., m}
# voters {0, 1, ..., n}
import numpy as np 

class Voters:
    def __init__(self, numVoters, numCandidates, polarizing):
        self.numVoters = numVoters
        self.numCandidates = numCandidates
        self.isPolarizing = polarizing

    def getRankedPreferences(self):
        return self.getRankedPolarizing() if self.isPolarizing else self.getRankedRandom()

    # preferences is dictionary from tuple -> int
    def getRankedRandom(self):
        preferences = {}
        for i in range(self.numVoters):
            onePreference = tuple(np.random.permutation(self.numCandidates))
            if onePreference in preferences.keys():
                preferences[onePreference] += 1
            else:
                preferences[onePreference] = 1
        return preferences

    def getRankedPolarizing(self):
        pass

    def getMajorityPreferences(self):
        return self.getMajorityPolarizing() if self.isPolarizing else self.getMajorityRandom()

    # preferences is dictionary from int -> int
    def getMajorityRandom(self):
        preferences = {k:0 for k in range(self.numCandidates)}
        for i in range(self.numVoters):
            randomCandidate = np.random.randint(0, self.numCandidates)
            preferences[randomCandidate] += 1
        return preferences

    def getMajorityPolarizing(self):
        pass

    # preferences is dictionary from tuple -> int
    def getApprovalPreferences(self):
        preferences = {}
        func = lambda i: np.fabs(1.0 / (0.7 + 0.3 * np.exp((i+1) * (i != 0))))
        candVec = np.zeros(self.numCandidates-1)
        total = np.asarray([func(i) for i in range(self.numCandidates)])
        total = total * self.numVoters / np.sum(total) # number of voters voting for one candidate, two candidates, ... n candidates
        total = np.round(total)
        for i in range(self.numCandidates):
            # choose i + 1 indices to be 1, all others 0
            for j in range(np.int(total[i])):
                arr = np.zeros(self.numCandidates)
                ones = np.random.choice(self.numCandidates, i + 1, replace = False)
                arr[ones] = 1
                onePreference = tuple(arr)
                if onePreference in preferences.keys():
                    preferences[onePreference] += 1
                else:
                    preferences[onePreference] = 1
        return preferences

# myV = Voters(10000, 6, False)
# print(myV.getApprovalPreferences())


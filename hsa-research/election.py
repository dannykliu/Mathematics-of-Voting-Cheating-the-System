from voters import Voters
import numpy as np 

class Election:
    def __init__(self, numVoters, numCandidates, polarizing):
        self.voters = Voters(numVoters, numCandidates, polarizing)
        self.numCandidates = numCandidates
        self.rankedPreferences = self.voters.getRankedPreferences()
        self.majorityPreferences = self.voters.getMajorityPreferences()
        self.approvalPreferences = self.voters.getApprovalPreferences()

    # helper function
    def getPreferences(self, prefType):
        points, preferences = {k:0 for k in range(self.numCandidates)}, None
        if prefType == 'ranked':
            preferences = self.rankedPreferences
        elif prefType == 'approval':
            preferences = self.approvalPreferences
        else:
            raise Exception('Illegal preference type')
        return points, preferences

    # return the winner of the election under majority rule
    def getMajority(self):
        return max(self.majorityPreferences, key=self.majorityPreferences.get)

    # returns the winner of the election under borda count
    def getBorda(self):
        points, preferences = self.getPreferences('ranked')
        for preference in preferences:
            n = self.numCandidates
            for candidate in preference:
                points[candidate] += preferences[preference] * n
                n -= 1
        return max(points, key=points.get)

    # recursively find winner of instant runoff
    def recurIRV(self, points, preferences):
        if len(points) == 2:
            return max(points, key=points.get)
        loser = min(points, key=points.get)
        #print('candidate %d is eliminated' % loser)
        points.pop(loser) # get rid of loser
        newPreferences = {}
        for preference in preferences:
            if preference[0] == loser:
                points[preference[1]] += preferences[preference] # transfer votes of loser
            _list = list(preference)
            _list.remove(loser)
            _preference = tuple(_list)
            newPreferences[_preference] = preferences[preference]
        return self.recurIRV(points, newPreferences)

    # returns winner of election under instant runoff voting
    def getIRV(self):
        points, preferences = self.getPreferences('ranked')
        #preferences = {(0, 1, 2, 3): 10, (1, 0, 2, 3): 5, (2, 0, 1, 3): 4}
        for preference in preferences:
            points[preference[0]] += preferences[preference] # count first place votes on first election
        return self.recurIRV(points, preferences)

    # returns winner of election under approval voting
    def getApproval(self):
        points, preferences = self.getPreferences('approval')
        #preferences = {(1, 1, 0): 1, (1, 0, 1): 1, (0, 0, 1): 2}
        for preference in preferences:
            _list = list(preference)
            indexOO = [i for i, x in enumerate(_list) if x == 1]
            for index in indexOO:
                points[index] += preferences[preference]
        return max(points, key=points.get)

    def getMajorityLoss(self):
        winner = self.getMajority()
        loss = 0
        for preference in self.majorityPreferences:
            if preference != winner:
                loss += self.majorityPreferences[preference] 
        return loss

    def getApprovalLoss(self):
        winner = self.getApproval()
        loss = 0
        for preference in self.approvalPreferences:
            loss += preference[winner] == 1
        return loss

    def getRankedLoss(self, winner, preferences):
        loss = 0
        scale = np.arange(self.numCandidates) / (self.numCandidates - 1)
        for preference in preferences:
            _preference = list(preference)
            indOfWinner = _preference.index(winner)
            loss += preferences[preference] * scale[indOfWinner]
        return loss

    def getBordaLoss(self):
        return self.getRankedLoss(self.getBorda(), self.rankedPreferences)

    def getIRVLoss(self):
        return self.getRankedLoss(self.getIRV(), self.rankedPreferences)


borda, irv, majority, approval = 0, 0, 0, 0
for i in range(1000):
    myE = Election(100, 5, False)
    borda += myE.getBordaLoss()/1000
    irv += myE.getIRVLoss()/1000
    majority += myE.getMajorityLoss()/1000
    approval += myE.getApprovalLoss()/1000

print(borda, irv, majority, approval)

'''
intro to a story... from the perspective of a 
'''

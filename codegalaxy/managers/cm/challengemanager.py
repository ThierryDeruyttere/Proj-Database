import dbw
from managers.cm.Challenges import *

class ChallengeManager:

    def __init__(self):
        pass

    def createChallenge(self, challenger_id, challenged_id, challenge_type, list_id):
        challenge = None
        if challenge_type == "Score":
            challenge = 1
        elif challenge_type == "Perfects":
            challenge = 2

        dbw.createChallenge(challenger_id, challenged_id, challenge, list_id)


    def getChallengeRequestsForUser(self, user_id, language_id):
        requests = dbw.getChallengeForStatus(user_id, "Pending")
        challenges = []
        for i in requests:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'] ,i['list_id'], i['status'], language_id))

        return challenges


    def cancelChallenge(self, challenger_id, challenged_id, list_id):
        dbw.cancelChallenge(challenger_id, challenged_id, list_id)

    def acceptChallenge(self, challenger_id, challenged_id, list_id):
        dbw.acceptChallenge(challenger_id, challenged_id, list_id)

    def getActiveChallengesForUser(self,user_id, language_id):
        active = dbw.getChallengeForStatus(user_id, "Accepted")
        challenges = []
        for i in active:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'] ,i['list_id'], i['status'], language_id))

        return challenges


    def getFinishedChallengesForUser(self, user_id, language_id):
        #First check if there are some active challenges that are finished
        active = self.getActiveChallengesForUser(user_id, language_id)
        for challenge in active:
            if challenge.isFinished():
                print("finished")

        finished = dbw.getChallengeForStatus(user_id, "Finished")
        challenges = []
        for i in finished:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'] ,i['list_id'], i['status'], language_id))

        #Add rest of logic



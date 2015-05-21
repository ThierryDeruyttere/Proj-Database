import dbw
from managers.cm.Challenges import *

class ChallengeManager:

    def __init__(self):
        pass

    def getChallengesBetween(self, challenger_id, challenged_id, language_id):
        requests = dbw.getChallengesBetween(challenger_id, challenged_id)
        challenges = []
        for i in requests:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'] ,i['list_id'], i['status'], language_id))

        return challenges

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

    def updateActiveChallengesForUser(self, user_id):
        self.getActiveChallengesForUser(user_id, 1)


    def getActiveChallengesForUser(self,user_id, language_id):
        active = dbw.getChallengeForStatus(user_id, "Accepted")
        challenges = []
        for i in active:
            challenge = Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'] ,i['list_id'], i['status'], language_id)
            if not challenge.isFinished():
                challenges.append(challenge)
            else:
                challenge.finishChallenge()

        return challenges

    def checkActiveChallenges(self, user_id, language_id):
        #checks if active challenges are finished
        active = self.getActiveChallengesForUser(user_id, language_id)
        for challenge in active:
            if challenge.isFinished():
                challenge.finishChallenge()

    def getFinishedChallengesForUser(self, user_id, language_id):
        self.checkActiveChallenges(user_id, language_id)

        finished = dbw.getChallengeForStatus(user_id, "Finished")
        challenges = []
        for i in finished:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'] ,i['list_id'], i['status'], language_id, i['winner_id']))

        return challenges

    def giveUpChallenge(self, user_id, challenger_id, challenged_id, list_id):
        winner = None
        if user_id == challenger_id:
            winner = challenged_id
        else:
            winner = challenger_id

        dbw.finishChallenge(challenger_id, challenged_id, list_id, winner)

    def getWinsAgainst(self, first_user, second_user):
        return len(dbw.getChallengeWinsAgainst(first_user, second_user))

    def getFinishedChallengesBetween(self, first_user, second_user, language_id):
        active = dbw.getFinishedChallengesBetween(first_user, second_user)
        challenges = []
        for i in active:
            challenge = Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'] ,i['list_id'], i['status'], language_id)
            challenges.append(challenge)

        return challenges
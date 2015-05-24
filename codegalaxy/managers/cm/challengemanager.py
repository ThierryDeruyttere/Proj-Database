import dbw
from managers.cm.Challenges import *

# Object that will be used to update/query info on challenges (mostly used in views)
class ChallengeManager:

    def __init__(self):
        pass

    # Returns the challenges that are busy, finished or even just requested
    # between two users
    def getChallengesBetween(self, challenger_id, challenged_id, language_id):
        requests = dbw.getChallengesBetween(challenger_id, challenged_id)
        challenges = []
        for i in requests:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'], i['list_id'], i['status'], language_id))

        return challenges

    # Adds a challenge to the database
    def createChallenge(self, challenger_id, challenged_id, challenge_type, list_id):
        challenge = None
        if challenge_type == "Score":
            challenge = 1
        elif challenge_type == "Perfects":
            challenge = 2

        dbw.createChallenge(challenger_id, challenged_id, challenge, list_id)

    # Gets all the challenge requests for a certain user
    def getChallengeRequestsForUser(self, user_id, language_id):
        requests = dbw.getChallengeForStatus(user_id, "Pending")
        challenges = []
        for i in requests:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'], i['list_id'], i['status'], language_id))

        return challenges

    # Deletes a requested challenge from the database (by not accepting)
    def cancelChallenge(self, challenger_id, challenged_id, list_id):
        dbw.cancelChallenge(challenger_id, challenged_id, list_id)

    # Starts a requested challenge by updating it
    def acceptChallenge(self, challenger_id, challenged_id, list_id):
        dbw.acceptChallenge(challenger_id, challenged_id, list_id)

    # Gets all currently active challenges for a certain user
    def getActiveChallengesForUser(self, user_id, language_id):
        active = dbw.getChallengeForStatus(user_id, "Accepted")
        challenges = []
        for i in active:
            challenge = Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'], i['list_id'], i['status'], language_id)
            challenges.append(challenge)

        return challenges

    # checks if any active challenges are finished, and if so, "marks" them as such
    def checkActiveChallenges(self, user_id, language_id):
        # List of active challenges for a user
        active = self.getActiveChallengesForUser(user_id, language_id)
        for challenge in active:
            if challenge.isFinished():
                challenge.finishChallenge()

    # Gets all finished challenges for a certain user
    def getFinishedChallengesForUser(self, user_id, language_id):
        # First we check if any active challenges are finished
        self.checkActiveChallenges(user_id, language_id)

        # Then we search the database
        finished = dbw.getChallengeForStatus(user_id, "Finished")
        challenges = []
        for i in finished:
            challenges.append(Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'], i['list_id'], i['status'], language_id, i['winner_id']))

        return challenges

    # Gives up on a challenge (and thereby giving the other player the win)
    def giveUpChallenge(self, user_id, challenger_id, challenged_id, list_id):
        winner = None
        if user_id == challenger_id:
            winner = challenged_id
        else:
            winner = challenger_id

        dbw.finishChallenge(challenger_id, challenged_id, list_id, winner)

    # Gets the amount of wins a user has against another user
    def getWinsAgainst(self, first_user, second_user):
        return len(dbw.getChallengeWinsAgainst(first_user, second_user))

    # Returns the finished Challenges between two users
    def getFinishedChallengesBetween(self, first_user, second_user, language_id):
        active = dbw.getFinishedChallengesBetween(first_user, second_user)
        challenges = []
        for i in active:
            challenge = Challenge(i['challenger_id'], i['challenged_id'], i['challenge_type_id'], i['list_id'], i['status'], language_id)
            challenges.append(challenge)

        return challenges

import dbw
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
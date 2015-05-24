from managers.om import *
object_manager = objectmanager.ObjectManager()
import dbw

class ChallengeType:

    def __init__(self, code):
        self.code = code
        if self.code == 1:
            self.type = "Score"
        elif self.code == 2:
            self.type = "Perfects"

class Challenge:

    def __init__(self, challenger, challenged, challenge_type, list_id, status, language_id, winner=None):
        # The users in the challege as objects
        self.challenger = object_manager.createUser(id=challenger)
        self.challenged = object_manager.createUser(id=challenged)
        self.challenge_type = challenge_type
        # if we passed a string or int, quickly create Challenge type object
        if not isinstance(challenge_type, ChallengeType):
            self.challenge_type = ChallengeType(challenge_type)
        self.status = status
        self.winner = object_manager.createUser(id=winner)
        self.list = object_manager.createExerciseList(list_id, language_id)

    # Returns a boolean that tells us if the list is finished
    def isFinished(self):
        if self.status == "Finished":
            return True

        # Check if both users finished the list
        if self.challenger.haveImadeList(self.list.id) and self.challenged.haveImadeList(self.list.id) and self.status == "Accepted":
            return True

        return False

    # Chacks which user has the higher score and chooses the winner acordingly
    def selectWinner(self, challenger_score, challenged_score):
        if challenger_score > challenged_score:
            self.winner = self.challenger
        elif challenger_score < challenged_score:
            self.winner = self.challenged
        else:
            # ex eaquo...
            self.winner = self.challenger

    # Will set the challenge as finished and will give scores based on
    # the challenge type. After this it will use the above function to select a winner
    def finishChallenge(self):
        self.status = "Finished"
        # Determine winner

        # Set the score of each user when you're done with your if statement
        # At the end of the function, the victor is chosen.
        challenger_score = 0
        challenged_score = 0

        challenger_list = self.challenger.personalListWithId(self.list.id, 1)
        challenged_list = self.challenged.personalListWithId(self.list.id, 1)
        if self.challenge_type.code == 1:
            # Score game mode
            challenger_score = challenger_list.score
            challenged_score = challenger_list.score

        elif self.challenge_type.code == 2:
            # Perfects gamemode

            # language code doesn't matter here
            challenger_exercises = challenger_list.allExercises('en')
            challenged_exercises = challenged_list.allExercises('en')

            # This could be done in one loop, but what if a user adds more exercises to a list
            # when one of the two players has already finished the list?
            for i in challenger_exercises:

                if i.score == i.max_score:
                    challenger_score += 1

            for i in challenged_exercises:
                if i.score == i.max_score:
                    challenged_score += 1

        self.selectWinner(challenger_score, challenged_score)
        dbw.finishChallenge(self.challenger.id, self.challenged.id, self.list.id, self.winner.id)

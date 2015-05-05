from managers.om import *
object_manager = objectmanager.ObjectManager()

class ChallengeType:
    def __init__(self, type):
        self.code = None
        self.type = None
        if isinstance(type, str):
            self.createFromStr(type)

        elif isinstance(type, int):
            self.createFromInt(type)

    def createFromInt(self, code):
        self.code = code
        if self.code == 1:
            self.type = "Score"
        elif self.code == 2:
            self.type = "Perfects"

    def createFromStr(self, str):
        self.type = str
        self.code = 0
        if  self.type == "Score":
            self.code = 1
        elif self.type == "Perfects":
            self.code = 2



class Challenge:
    def __init__(self, challenger, challenged, challenge_type,list_id, status, language_id, winner=None):
        self.challenger = object_manager.createUser(id=challenger)
        self.challenged = object_manager.createUser(id=challenged)
        self.challenge_type = challenge_type
        #if we passed a string or int, quickly create Challenge type object
        if not isinstance(challenge_type, ChallengeType):
            self.challenge_type = ChallengeType(challenge_type)
        self.status = status
        self.winner = object_manager.createUser(id=winner)
        self.list = object_manager.createExerciseList(list_id,language_id)

    def isFinished(self):
        if self.status == "Finished":
            return True

        #Check if both users finished the list
        if self.challenger.haveImadeList(self.list.id) and self.challenged.haveImadeList(self.list.id) and self.status == "Accepted":
            return True

        return False

    def FinishChallenge(self):
        self.status = "Finished"
        #Determine winner
        if self.challenge_type.code == 1:
            #Score game mode
            challenger_list_data = self.challenger.personalListWithId(self.list.id)
            challenged_list_data = self.challenged.personalListWithId(self.list.id)
            if challenged_list_data.score > challenger_list_data.score:
                self.winner = self.challenged
            elif challenged_list_data.score < challenger_list_data.score:
                self.winner = self.challenger
            else:
                #ex eaquo...
                #Meh challenger wins >:D
                self.winnder = self.challenger
        elif self.challenge_type.code == 2:
            #Perfects gamemode
            pass
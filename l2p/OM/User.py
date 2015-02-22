# Laten inheriten van Exercise/ExerciseList?

class PersonalList:
    def __init__(self):
        # List of PersonalExercises
        self.excersises_list
        # Integer representing the number of the last-made excersise (needed?)
        self.last_made
        #given rating
        self.rating
        # total obtained score
        self.score
        self.excersise_list


        # Object which represents the actual list of exercises (SQL function)
        def allExercises():
            pass


class PersonalExercise:
    def __init__(self):
        # bool to check if exercise was solved
        self.solved
        # obtained score
        self.score
        # given rating
        self.rating
        # Object which represents the actual excersise
        self.excersise

class User:
    def __init__(self):
        # List with other users this user is befriended with
        self.friends_list

        # Plain info on the user
        self.id
        self.first_name
        self.last_name
        self.is_active
        self.account_name
        self.email

        # password not needed here?



        self.personal_lists

        self.permissions

        # List with all the groups this user is currently in (SQL function)
        def getGroups():
            pass

        # List with all the lists of exercises this user has completed/is working on (SQL function)
        def personalLists():
            pass

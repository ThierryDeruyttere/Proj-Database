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
        # Object which represents the actual list
        self.excersise_list



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

        # Map with groupIDs this user is in + the permissions for that group
        self.groups

        # List with all the lists of exercises this user has completed/is working on
        self.personal_lists

        self.permissions

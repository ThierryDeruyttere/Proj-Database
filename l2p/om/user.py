import om.exerciselist
import om.exercise
import dbw

class User:
    def __init__(self,id,first_name,last_name,is_active,email,permissions):
        # Plain info on the user
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.email = email
        # password not needed here?
        self.permissions = permissions


        # List with other users this user is befriended with
        def allFriends(self):
            pass

        # List with all the groups this user is currently in (SQL function)
        def allGroups(self):
            pass

        # List with all the lists of exercises this user has completed/is working on (SQL function)
        def allPersonalLists(self):
            pass

        # returns TRUE for admin and FALSE for regular user
        def checkPermission(self,group_id):
            pass


class PersonalList:
    def __init__(self,rating,score,exercise_list_id,user_id):
        #given rating
        self.rating = rating
        # total obtained score
        self.score = score
        # Needed to use the allExercises function
        self.user_id = user_id
        # Actual exercises-object (make with SQL queries)
        self.excersises_list
        # Integer representing the number of the last-made excersise (needed?) ("calculate" with the real list-obj)
        self.last_made

        # Object which represents the actual list of personal exercises (SQL function)
        def allExercises(self):
            pass


class PersonalExercise:
    def __init__(self,solved,score,rating,exercise_id):
        # bool to check if exercise was solved
        self.solved = solved
        # obtained score
        self.score = score
        # given rating
        self.rating = rating
        # Object which represents the actual excersise (make with SQL query)
        self.excersise

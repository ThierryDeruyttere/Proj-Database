import om.exerciselist
import om.exercise
import om.user
import om.group
import dbw
# Class that will build and work with the various objects representing the site
# will use SQL


class ObjectManager:
    '''Class which will consist of a few make-functions for objects by using SQL queries
    then some info-gathering functions for the views'''
    def __init__(self):
        pass

    # NOTE: create functions return the object created OR None if the ID does not exist

    # Uses the DB to create an object representing a user
    def createUser(self, **kwargs):
        # Get search key from kwargs, only one possible key atm
        user_info = None
        if 'id' in kwargs:
            user_info = dbw.getUserOnId(kwargs['id'])
        elif 'email' in kwargs:
            user_info = dbw.getUserOnEmail(kwargs['email'])
        if user_info:
            user_object = om.user.User(user_info['id'],user_info['first_name'],user_info['last_name'],
            user_info['is_active'],user_info['email'],user_info['permission'], user_info['password'])
            return user_object
        else:
            return None

#TODO: De volgende creates afmaken: Exercise

    # Uses the DB to create an object representing a Group
    def createGroup(self,id):
        group_info = dbw.getGroupInformation(id)
        if group_info:
            group_object = om.group.Group(id,group_info['group_name'],group_info['group_type'])
            return group_object
        else:
            return None

    # Uses the DB to create an object representing an Exercise
    def createExercise(self,id):
        exercise_info = dbw.getExerciseInformation(id)
        if exercise_info:
            exercise_object = om.exercise.Exercise(id,exercise_info['difficulty'],
            exercise_info['max_score'],exercise_info['penalty'],exercise_info['exercise_type'])
            return exercise_object
        else:
            return None

    # Uses the DB to create an object representing a ExerciseList
    def createExerciseList(self,id):
        exercise_list_info = dbw.getExerciseListInformation(id)
        if exercise_list_info:
            exercise_list_object = om.exerciselist.ExerciseList(id,exercise_list_info['name'],
            exercise_list_info['difficulty'],exercise_list_info['description'])
            return exercise_list_object
        else:
            return None

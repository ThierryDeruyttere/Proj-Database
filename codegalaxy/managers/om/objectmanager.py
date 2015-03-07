import managers.om.exerciselist
import managers.om.exercise
import managers.om.user
import managers.om.group
import dbw
# Class that will build and work with the various objects representing the site
# will use SQL


class ObjectManager:
    '''Class which will consist of a few make-functions for objects by using SQL queries
    then some info-gathering functions for the views'''
    def __init__(self):
        pass

    # CREATE functions make an object with Data from the DB-SQL Queries

    # NOTE: create functions return the object created OR None if the ID does not exist

    # Uses the DB to create an object representing a user
    def createUser(self, **kwargs):
        # Get search key from kwargs, only one possible key atm
        user_info = None
        if 'id' in kwargs and kwargs['id']:
            user_info = dbw.getUserOnId(kwargs['id'])
        elif 'email' in kwargs and kwargs['email']:
            user_info = dbw.getUserOnEmail(kwargs['email'])

        if user_info:
            user_object = managers.om.user.User(user_info['id'],user_info['first_name'],user_info['last_name'],
            user_info['is_active'],user_info['email'],user_info['permission'], user_info['password'])
            return user_object
        else:
            return None

    # Uses the DB to create an object representing a Group
    def createGroup(self,id):
        group_info = dbw.getGroupInformation(id)
        if group_info:
            group_object = managers.om.group.Group(id,group_info['group_name'],group_info['group_type'],group_info['created_on'])
            return group_object
        else:
            return None

    # Uses the DB to create an object representing an Exercise
    def createExercise(self,id,language_code):
        exercise_info = dbw.getExerciseInformation(id,language_code)
        if exercise_info:
            exercise_object = managers.om.exercise.Exercise(id,exercise_info['difficulty'],
            exercise_info['max_score'],exercise_info['penalty'],exercise_info['exercise_type']
            ,exercise_info['programming_language'],exercise_info['code_text'],exercise_info['question_text']
            ,language_code,exercise_info['correct_answer'],exercise_info['language_name'], exercise_info['title'])
            return exercise_object
        else:
            return None

    # Uses the DB to create an object representing a ExerciseList
    def createExerciseList(self,id):
        exercise_list_info = dbw.getExerciseListInformation(id)
        if exercise_list_info:

            exercise_list_object = managers.om.exerciselist.ExerciseList(id,exercise_list_info['name'],
            exercise_list_info['difficulty'],exercise_list_info['description'],
            exercise_list_info['created_by'], exercise_list_info['created_on'],
            exercise_list_info['prog_lang_id'])
            return exercise_list_object
        else:
            return None


    # INSERT functions will insert info into the DB by calling dbw functions

    def insertUser(self,first_name, last_name, email, password):
        dbw.insertUser(first_name, last_name,password, email)

    def insertExerciseList(self,name, description ,difficulty,created_by,created_on,prog_lang_name):
        prog_lang_id = dbw.getIdFromProgrammingLanguage(prog_lang_name)["id"]
        return dbw.insertExerciseList(name, description ,difficulty,created_by,created_on,prog_lang_id)["highest_id"]

    def insertGroup(self,group_name, group_type,created_on):
        dbw.insertGroup(group_name, group_type,created_on)

    def allProgrammingLanguages(self):
        return dbw.getAll("programmingLanguage")
        # do you just need the name? id?
        #return [x['name'] for x in dbw.getAll("programmingLanguage")]

    def allUsers(self):
        users = []
        user_info = dbw.getAllUserIDs()
        for user_id in user_info:
            users.append(self.createUser(id = user_id['id']))
        return users

    def allGroups(self):
        groups = []
        group_info = dbw.getAllGroupIDs()
        for group_id in group_info:
            groups.append(self.createGroup(id = group_id['id']))
        return groups

    def countExerciseListsForProgrammingLanguageID(self,id):
        return dbw.countExerciseListsForProgrammingLanguageID(id)


    def userMadeExercise(self, exercise_id, user_id, exercise_score, made_exercise, rating=0):
        exercise = dbw.getMadeExericse(user_id, exercise_id)
        if exercise:
            #update
            pass

        else:
            dbw.insertMadeExercise(user_id,exercise_id, made_exercise, exercise_score, rating)

    def getInfoForUserForExericse(self, exercise_id, user_id):
        return dbw.getMadeExericse(user_id, exercise_id)

    def addSubject(self, name):
         dbw.insertSubject(name)

    def getIdOfSubject(self,name):
        return dbw.getSubjectID(name)["id"]

    def needsVerification(self, hash):
        return dbw.needsVerification(hash)

    def addVerification(self, email, hash):
        dbw.addVerification(email, hash)

    def acceptVerification(self, hash):
        dbw.removeVerification(hash)

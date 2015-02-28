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
            exercise_info['max_score'],exercise_info['penalty'],exercise_info['exercise_type']
            ,exercise_info['programming_language'],exercise_info['code_text'],exercise_info['question_text']
            ,exercise_info['language'],exercise_info['answer_text'])
            return exercise_object
        else:
            return None

    # Uses the DB to create an object representing a ExerciseList
    def createExerciseList(self,id):
        exercise_list_info = dbw.getExerciseListInformation(id)
        if exercise_list_info:
            exercise_list_object = om.exerciselist.ExerciseList(id,exercise_list_info['name'],
            exercise_list_info['difficulty'],exercise_list_info['description'],
            exercise_list_info['created_by'], exercise_list_info['created_on'],
            exercise_list_info['prog_lang_id'])
            return exercise_list_object
        else:
            return None


    # ADD functions will insert info into the DB by calling dbw functions

    def addUser(self,first_name, last_name, email, password):
        dbw.insertUser(first_name, last_name,password, email)

    def addExerciseToList(self,difficulty, max_score, penalty, exercise_type,created_by
        , created_on, exercise_number,programming_language,question,answers,correct_answer
        ,hints,list_id,code = ""):
        # Info for exercises table + id of the exercise
        exercise_id = dbw.insertExercise(difficulty, max_score, penalty, exercise_type
        ,created_by, created_on, exercise_number)['highest_id']
        # AssociatedWith relation
        pl_id = dbw.getIdFromProgrammingLanguage(programming_language)['id']
        dbw.insertAssociatedWith(pl_id,exercise_id)
        # Code (default "")
        dbw.insertCode(code,exercise_id)
        # question = QuestionContainer object
        dbw.insertQuestion(question.question_text, question.language_id, exercise_id)
        # answers is a list of AnswerContainer objects (see below)
        for answer in answers:
            # TODO: fix this
            dbw.insertAnswer(answer.answer_number, answer.answer_text, answer.language_id, answer.is_answer_for)
        # TODO :correct_answer -> changes to answer needed so i'll hold off on this
        # hints, like answers, is a list of HintContainer objects
        for hint in hints:
            dbw.insertHint(hint.hint_text, hint.hint_number, hint.exercise_id)
        # Linking exercise+list
        dbw.insertIsPartOf(list_id, exercise_id)

    def addExerciseList(self,name, description ,difficulty):
        dbw.insertExerciseList(name, description ,difficulty)

    def addGroup(self,group_name, group_type):
        dbw.insertGroup(group_name, group_type)

    def addMemberToGroup(self,group_id, user_id, user_permissions):
        dbw.insertUserInGroup(group_id, user_id, user_permissions)



# NOTE : Make these with the info stored in the HTML boxes
class AnswerContainer():
    def __init__(self,answer_number, answer_text, language_id, is_answer_for):
        self.answer_number = answer_number
        self.answer_text = answer_text
        self.language_id = language_id
        self.is_answer_for = is_answer_for

# NOTE : Make these with the info stored in the HTML boxes
class HintContainer():
    def __init__(self,hint_text, hint_number, exercise_id):
        self.hint_text = hint_text
        self.hint_number = hint_number
        self.exercise_id = exercise_id

class QuestionContainer():
    def __init__(self,question_text,language_id):
        self.question_text = question_text
        self.language_id = language_id

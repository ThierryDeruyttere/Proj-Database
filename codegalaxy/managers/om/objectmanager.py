import managers.om.exerciselist
import managers.om.exercise
import managers.om.user
import managers.om.group
import managers.om.feed
import managers.om.badge
import dbw
import datetime
# Class that will build and work with the various objects representing the site
# will use SQL


def timeFromToday(compare_date):
    compare_date = compare_date.replace(tzinfo=None)
    now = datetime.datetime.now()
    return compare_date - now

class Language:

    def __init__(self, id, name, code=None):
        self.id = id
        self.name = name
        self.code = code

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
            badge = self.createBadge(user_info['badge_id'])
            user_object = managers.om.user.User(user_info['id'], user_info['first_name'], user_info['last_name'],
                                                user_info['is_active'], user_info['email'], user_info['permission'], user_info['password'], user_info['joined_on'], user_info['last_login'], user_info['gender'], badge)
            return user_object
        else:
            return None

    # Uses the DB to create an object representing a Group
    def createGroup(self, id):
        group_info = dbw.getGroupInformation(id)
        if group_info:
            group_object = managers.om.group.Group(id, group_info['group_name'], group_info['group_type'], group_info['created_on'])
            return group_object
        else:
            return None

    def createBadge(self, id):
        badge_info = dbw.getBadgeInformation(id)
        if badge_info:
            badge_object = managers.om.badge.Badge(id, badge_info['name'], badge_info['type'], badge_info['message'], badge_info['target_value'], badge_info['medal'])
            return badge_object
        else:
            return None

    def getAllBadges(self):
        badges_info = dbw.getAllBadgeInformation()
        badges=[]

        for badge_info in badges_info:
            badge_object = managers.om.badge.Badge(badge_info['id'], badge_info['name'], badge_info['type'], badge_info['message'], badge_info['target_value'], badge_info['medal'])
            badges.append(badge_object)

        return badges

    def getAllBadgesOnMedal(self):
        badges_info = dbw.getAllBadgeInformation()
        badges={}
        gold = []
        silver = []
        bronze = []
        for badge_info in badges_info:
            badge_object = managers.om.badge.Badge(badge_info['id'], badge_info['name'], badge_info['type'], badge_info['message'], badge_info['target_value'], badge_info['medal'])
            if badge_object.medal == 'gold':
                gold.append(badge_object)
            elif badge_object.medal == 'silver':
                silver.append(badge_object)
            elif badge_object.medal == 'bronze':
                bronze.append(badge_object)

        badges['gold'] = gold
        badges['silver'] = silver
        badges['bronze'] = bronze
        return badges

    def createGroupOnName(self, group_name):
        group_info = dbw.getGroupInformationOnName(group_name)
        if group_info:
            group_object = managers.om.group.Group(group_info['id'], group_name, group_info['group_type'], group_info['created_on'])
            return group_object
        else:
            return None

    # Uses the DB to create an object representing an Exercise
    def createExercise(self, id, language_code='en'):
        exercise_info = dbw.getExerciseInformation(id, language_code)

        if language_code != 'en' and exercise_info is None:
            exercise_info = dbw.getExerciseInformation(id, 'en')
        if exercise_info:
            exercise_object = managers.om.exercise.Exercise(id,
                                                            exercise_info['max_score'], exercise_info['penalty'], exercise_info['exercise_type'], exercise_info['programming_language'], exercise_info['code_text'], exercise_info['question_text'], language_code, exercise_info['correct_answer'], exercise_info['language_name'], exercise_info['title'], exercise_info['created_by'], exercise_info['created_on'], exercise_info['exercise_number'], exercise_info['exerciseList_id'])
            return exercise_object
        else:
            return None

    # Uses the DB to create an object representing a ExerciseList
    def createExerciseList(self, id, lang_id):
        exercise_list_info = dbw.getExerciseListInformation(id, lang_id)
        if exercise_list_info:

            exercise_list_object = managers.om.exerciselist.ExerciseList(id, exercise_list_info['name'],
                                                                         exercise_list_info['difficulty'], exercise_list_info['description'],
                                                                         exercise_list_info['created_by'], exercise_list_info['created_on'],
                                                                         exercise_list_info['prog_lang_id'])
            return exercise_list_object
        else:
            return None

# INSERT functions will insert info into the DB by calling dbw functions
    def insertUser(self, first_name, last_name, email, password, joined_on, last_login, gender):
        dbw.insertUser(first_name, last_name, password, email, 0, joined_on, last_login, gender)

    def registered(self, email):
        user = self.createUser(email=email)
        dbw.incrementBadgeValue(user.id, 'timeMember')

    def insertExerciseList(self, name, description, difficulty, created_by, created_on, prog_lang_name, lang_id, translations):
        prog_lang_id = dbw.getIdFromProgrammingLanguage(prog_lang_name)["id"]
        highest_id = dbw.insertExerciseList(name, description, difficulty, created_by, created_on, prog_lang_id, lang_id)["highest_id"]
        for lang, val in translations.items():
            if val:
                dbw.insertListTranslation(val['name'], val['description'], int(highest_id), lang.id)
        return int(highest_id)

    def insertGroup(self, group_name, group_type, created_on):
        dbw.insertGroup(group_name, group_type, created_on)

    def allProgrammingLanguages(self):
        return dbw.getAll("programmingLanguage")

    def allProgrammingLanguageIDs(self):
        return [x['id'] for x in dbw.getAll("programmingLanguage")]

    def allUsers(self):
        users = []
        user_info = dbw.getAllUserIDs()
        for user_id in user_info:
            users.append(self.createUser(id=user_id['id']))
        return users

    def allSubjectIDs(self):
        subjects = dbw.getAllSubjectIDs()
        return [subject['id'] for subject in subjects]

    def allGroups(self):
        groups = []
        group_info = dbw.getAllGroupIDs()
        for group_id in group_info:
            groups.append(self.createGroup(id=group_id['id']))
        return groups

    def allPublicGroups(self):
        groups = []
        group_info = dbw.getAllPublicGroupIDs()
        for group_id in group_info:
            groups.append(self.createGroup(id=group_id['id']))
        return groups

    def countExerciseListsForProgrammingLanguageID(self, id):
        return dbw.countExerciseListsForProgrammingLanguageID(id)

    def countExerciseListsForProgrammingLanguageIDMadeByUser(self, prog_lang_id, user_id):
        return dbw.countExerciseListsForProgrammingLanguageIDMadeByUser(prog_lang_id, user_id)

    def countExercisesForProgrammingLanguageIDMadeByUser(self, prog_lang_id, user_id):
        return dbw.countExercisesForProgrammingLanguageIDMadeByUser(prog_lang_id, user_id)

    def allSubjects(self):
        return dbw.getAllSubjects()

    def occurencesOfSubject(self, subject_id):
        return dbw.getOccurenceOfSubject(subject_id)

    def userMadeExercise(self, user_id, exercise_score, made_exercise, completed_on, list_id, exercise_number, last_answer="", hint=0):
        if hint is None:
            hint = 0
        exercise = dbw.getMadeExercise(user_id, list_id, exercise_number)
        if exercise:
            dbw.updateMadeExercise(list_id, user_id, exercise_number, last_answer, made_exercise, completed_on, hint, exercise_score)
        else:
            dbw.insertMadeExercise(user_id, made_exercise, exercise_score, completed_on, list_id, exercise_number, last_answer, hint)

    def getInfoForUserForExercise(self, user_id, exercise_list_id, exercise_number):
        return dbw.getMadeExercise(user_id, exercise_list_id, exercise_number)

    def addSubject(self, name):
        dbw.insertSubject(name)

    def getIdOfSubject(self, name):
        return dbw.getSubjectID(name)["id"]

    def needsVerification(self, hash):
        return dbw.needsVerification(hash)

    def addVerification(self, email, hash):
        dbw.addVerification(email, hash)

    def acceptVerification(self, hash):
        return dbw.getEmailFromVerificationAndRemoveVerification(hash)['email']

    def setUserActive(self, email):
        dbw.setUserActive(email)

    def filterOn(self, list_name='%', min_list_difficulty=1, max_list_difficulty=10, user_first_name='%', user_last_name='%', prog_lang_name='%', subject_name='%', order_mode='ASC', lang_id=1):
        lists = dbw.filterOn(list_name, min_list_difficulty, max_list_difficulty, user_first_name, user_last_name, prog_lang_name, subject_name, order_mode, lang_id)
        lists_objects = []
        for l in lists:
            lists_objects.append(self.createExerciseList(int(l['id']), lang_id))

        return lists_objects

    def getAllExerciseLists(self, language_id):
        all_prog_langs = self.allProgrammingLanguages()
        all_lists = []
        for i in all_prog_langs:
            lists = self.getExerciseListsOnProgLang(i["name"])
            for l in lists:
                all_lists.append(self.createExerciseList(l, language_id))

        return all_lists

    def getExerciseListsOnProgLang(self, prog_lang):
        lists = dbw.getExerciseListsOnProgLang(prog_lang)
        return [list_id['id'] for list_id in lists]

    def getAllScoresForList(self, exercise_list_id):
        scores = dbw.getAllScoresForList(exercise_list_id)
        return [score['score'] for score in scores]

    def amountOfLists(self):
        return len(dbw.allExerciseListIDs())

    def filterImportsLists(self, name):
        lists = dbw.filterLists(name)
        return [list_id['id'] for list_id in lists]

    def getOriginalExercise(self, list_id, exercise_number):
        return dbw.getOriginalExercise(list_id, exercise_number)['id']

    def getExerciseID(self, list_id, exercise_number):
        return dbw.getExerciseInList(list_id, exercise_number)['id']

    def getAllReferencesTo(self, exercise_id):
        return dbw.getAllReferencesToExercise(exercise_id)

    def getAllLanguages(self):
        languages = []
        for i in dbw.getAll('language'):
            languages.append(Language(i['id'], i['name'], i['language_code']))
        return languages

    def getLanguageObject(self, languade_code):
        lang = dbw.getLanguageForCode(languade_code)
        return Language(lang['id'], lang['name'], lang['language_code'])

    def getProgrLanguageObject(self, language_name):
        lang = dbw.getIdFromProgrammingLanguage(language_name)
        return Language(lang['id'], language_name)

    def getScoreForExerciseForUser(self, user_id, list_id, exercise_number):
        return dbw.getScoreForExerciseForUser(user_id, list_id, exercise_number)['exercise_score']

    def getUserByName(self, user_name):
        all_users = self.allUsers()
        for i in all_users:
            name = i.first_name + " " + i.last_name
            if name == user_name:
                return i
        return None

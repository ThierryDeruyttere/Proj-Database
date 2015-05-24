from django.db import connection
import time
from datetime import datetime

cursor = connection.cursor()

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def getAll(table):
    cursor = connection.cursor()
    cursor.execute('show tables like "{}"'.format(table))
    if len(dictfetchall(cursor)) > 0:
        cursor.execute('SELECT * FROM ' + table)
        fetched = dictfetchall(cursor)
        cursor.close()
        return fetched
    cursor.close()
    return None

def getUserOnId(id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user WHERE user.id = {}'.format(id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getUserOnEmail(email):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user WHERE user.email = "{}"'.format(email))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def processData(cursor):
    '''
    @brief gets the data from a sql query
    @return returns a list of dicts with the retrieved data
    '''
    info = dictfetchall(cursor)
    if not info:
        return []
    else:
        return info

def processOne(cursor):
    '''
    @brief gets the data from a sql query
    @return returns a dict with the retrieved data
    '''
    info = dictfetchall(cursor)
    if not info:
        return None
    else:
        return info[0]

def getListTranslation(id, language_id):
    '''
    @param id: the id of the list
    @param language_id: the id of the language
    @return returns the translation
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM listTranslation WHERE list_id = {id} AND language_id = {lang_id};'.format(id=id, lang_id=language_id))
    fetched = processOne(cursor)
    if fetched is None:
        cursor.execute('SELECT * FROM listTranslation WHERE list_id = {id} AND language_id = 1;'.format(id=id))
        fetched = processOne(cursor)
    cursor.close()
    return fetched

def getListsCreatedBy(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM exerciseList WHERE created_by = {user_id};'.format(user_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExerciseListInformation(id, lang_id):
    '''
    @brief get the information from Exercise lists given an user id
    @param id the id of the user
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM exerciseList WHERE id = {id};'.format(id=id))
    fetched = processOne(cursor)
    cursor.close()
    trans = getListTranslation(id, lang_id)
    if trans:
        fetched['name'] = trans['name']
        fetched['description'] = trans['description'].decode('utf-8')
    return fetched

def getExerciseListIdsMadeByUser(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM exerciseList WHERE created_by = {user_id};'.format(user_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getGroupUserPermissions(id, user_id):
    '''
    @brief get the permissions a user has in a group,
    @param id the id of the user, and the id of the group
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM userInGroup u WHERE u.group_id = {id} AND u.user_id = {user_id};'.format(id=id, user_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getGroupInformation(id):
    '''
    @brief get the information from Groups given an group id
    @param id the id of the group
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM groups WHERE id = {id};'.format(id=id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getGroupInformationOnName(group_name):
    '''
    @brief get the information from Groups given an group_name
    @param name of the group
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM groups WHERE group_name = "{group_name}";'.format(group_name=group_name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getUserInGroupInformation(group_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM userInGroup WHERE group_id = {group_id} AND user_id = {user_id};'.format(group_id=group_id, user_id=user_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getExerciseType(id):
    cursor = connection.cursor()
    cursor.execute('SELECT exercise_type FROM exercise WHERE id={id}'.format(id=id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getExerciseInformation(id, language_code):
    '''
    @brief get the information from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    exercise_type = getExerciseType(id)["exercise_type"]
    if exercise_type == "Open Question":
        cursor.execute('SELECT e.*, "" AS code_text, q.question_text, p.name AS programming_language, l.name AS language_name, eT.title FROM programmingLanguage p, exerciseList eL, exercise e, language l, question q, exerciseTitle eT WHERE e.id = {id} AND e.id = q.exercise_id AND q.language_id = l.id AND e.exerciseList_id = eL.id AND eL.prog_lang_id = p.id  AND l.language_code = "{lang_name}" AND eT.language_id = l.id AND eT.exercise_id = {id};'.format(id=id, lang_name=language_code))
    else:
        cursor.execute('SELECT e.*, c.code_text, q.question_text, p.name AS programming_language, l.name AS language_name, eT.title FROM programmingLanguage p, exerciseList eL, code c, exercise e, language l, question q, exerciseTitle eT WHERE e.id = {id} AND e.id = c.exercise_id  AND e.id = q.exercise_id AND q.language_id = l.id AND e.exerciseList_id = eL.id AND eL.prog_lang_id = p.id  AND l.language_code = "{lang_name}" AND eT.language_id = l.id AND eT.exercise_id = {id};'.format(id=id, lang_name=language_code))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getExerciseProgLanguage(id):
    '''
    @brief get the language from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT p.name FROM programmingLanguage p, exerciseList eL, exercise e WHERE e.id = {id} AND e.exerciseList_id = eL.id AND eL.prog_lang_id = p.id;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExerciseCode(id):
    '''
    @brief get the code from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT c.code_text FROM code c, exercise e WHERE e.id = {id} AND e.id = c.exercise_id;'.format(id=id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getExercQuestionAndLang(id):
    '''
    @brief get the Question and language from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT l.name, q.question_text FROM language l, question q, exercise e WHERE e.id = {id} AND e.id = q.exercise_id AND q.language_id = l.id;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExercCorrectAnswer(id, language_name):
    '''
    @brief get the information from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT a.answer_text, a.answer_number FROM answer a, exercise e, language l WHERE e.id = {id} AND e.id = a.is_answer_for AND e.correct_answer = a.answer_number AND l.name = {name} AND l.id = a.language_id;'.format(id=id, name=language_name))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getListsForUserId(user_id):
    '''
    @brief get the lists created by a certain user
    @param id the id of the user
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM  exerciseList  WHERE created_by = {id};'.format(id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExerciseAnswers(exercise_id, language_name):
    '''
    @brief get the answers for a Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with answers
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT a.answer_text, a.answer_number  FROM  answer a, exercise e, language l WHERE e.id = {id} AND a.is_answer_for = e.id AND a.language_id = l.id AND l.name = "{l_name}";'.format(id=exercise_id, l_name=language_name))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExerciseHints(id, languageName):
    '''
    @brief get the hints for a Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with hints
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT h.hint_text, h.hint_number  FROM exercise e, hint h, language l WHERE e.id = h.exercise_id AND e.id = {id} AND l.name = "{name}" AND l.id = h.language_id;'.format(id=id, name=languageName))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getFriendsIdForID(id):
    '''
    @brief gets the friends of a user a user id
    @param id the id of the user
    @return returns a dict with friends (hopefully)
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT f.friend_id, f.user_id FROM friendsWith f WHERE f.user_id = {id} UNION SELECT f.user_id, f.friend_id FROM friendsWith f WHERE f.friend_id = {id};'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getFriendsNotMemberOfGroupWithID(me_id, group_id):
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT u2.id FROM user u, user u2, friendsWith fW, userInGroup uIG, groups g WHERE g.id = {group_id} AND u.id = {me_id} AND u.id <> u2.id AND u2.id <> uIG.user_id AND uIG.group_id = g.id AND ((u.id = fW.user_id AND u2.id = fW.friend_id) OR (u2.id = fW.user_id AND u.id = fW.friend_id));'.format(me_id=me_id, group_id=group_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getFriendshipsForID(id):
    '''
    @brief gets the friends of a user a user id
    @param id the id of the user
    @return returns a dict with friendships
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM friendsWith f, user u WHERE f.user_id = {id} AND u.id = f.friend_id UNION SELECT * FROM friendsWith f, user u WHERE f.friend_id = {id} AND u.id = f.user_id;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getPendingFriendships(id):
    '''
    @brief gets the friendships of a user that are pending
    @param id the id of the user
    @return returns a dict with friendship and user
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM friendsWith f, user u WHERE f.friend_id = {id} AND status = "Pending" AND f.user_id = u.id ;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def defGetReversePendingFriendships(id):
    '''
    @brief gets the friendships of a user that are pending
    @param id the id of the user
    @return returns a dict with friendship and user
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM friendsWith f, user u WHERE f.user_id = {id} AND status = "Pending" AND f.friend_id = u.id ;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getPendingGroupMemberships(id):
    '''
    @brief get the groups of a user that are pending
    @param id the id of the user
    @return returns a dict with group
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM userInGroup u, groups g WHERE u.user_id = {id} AND u.status = "Pending" AND u.group_id = g.id ;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExercisesForList(list_id):
    '''
    @brief gets the exercises in a list given a list id
    @param id the id of the list
    @return returns a dict with exercises
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT e.id FROM exercise e WHERE e.exerciseList_id = {id};'.format(id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getEmailFromVerificationAndRemoveVerification(hash):
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM verification WHERE hash = "{hash}";'.format(hash=hash))
    result = processOne(cursor)
    cursor.execute('DELETE FROM verification WHERE hash = "{hash}";'.format(hash=hash))
    cursor.close()
    return result

def getExerciseReferencesForList(list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT e.original_id AS id,e.new_list_exercise_number FROM exercise_references e WHERE e.new_list_id = {id};'.format(id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getMadeListForUser(id):
    '''
    @brief gets the exercises list a user finished given a user id
    @param id the id of the user
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user u, madeList m WHERE  u.id = {id} AND u.id = m.user_id;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getMadeListForUser2(id):
    '''
    @brief gets the exercises list a user finished given a user id
    @param id the id of the user
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user u, madeList m, exerciseList e WHERE  u.id = {id} AND u.id = m.user_id AND m.exerciseList_id = e.id;'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def checkIfResultShared(user_id, list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM madeList m WHERE  m.user_id = {user_id} AND m.exerciseList_id = {list_id} AND m.shared = 1;'.format(user_id=user_id, list_id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getProgrammingLanguageIDsOfMadeExForUser(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT l.prog_lang_id FROM user u,exercise e, madeEx m, exerciseList l WHERE  u.id = {id} AND u.id = m.user_id AND m.exercise_number = e.exercise_number AND e.exerciseList_id = l.id AND m.list_id = l.id AND solved = 1;'.format(id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExerciseScoreFor(id, exercise_list):
    '''
    @brief gets the scores of exercises from a user in a certain exercise list
    @param id the id of the user
    @param exercise_list the id of the exercise list
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT e.id AS exercise_id, mE.solved, mE.exercise_score, mE.completed_on, mE.list_id, mE.exercise_number, mE.last_answer, e.max_score FROM user u, exerciseList eL, madeEx mE, exercise e WHERE u.id = {u_id} AND eL.id = {el_id} AND e.exerciseList_id = eL.id AND e.exerciseList_id =  mE.list_id AND e.exercise_number =  mE.exercise_number AND mE.user_id = u.id;'.format(u_id=id, el_id=exercise_list))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getSubjectsForList(list_id):
    '''
    @brief gets the subject of exercise list
    @param list_id the id of the exercise list
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT s.name FROM exerciseList e, subject s, hasSubject hS WHERE e.id = hS.exerciseList_id AND hS.subject_id = s.id AND e.id = {id};'.format(id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getSubjectIDsForList(list_id):
    '''
    @brief gets the subject of exercise list
    @param list_id the id of the exercise list
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT s.id FROM exerciseList e, subject s, hasSubject hS WHERE e.id = hS.exerciseList_id AND hS.subject_id = s.id AND e.id = {id};'.format(id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getPermForUserInGroup(user_id, group_id):
    '''
    @brief gets the permission for a certain user in a certain group
    @param user_id the id of the user
    @param group_id the id of the group
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT uIG.user_permissions FROM user u, groups g, userInGroup uIG WHERE u.id = {u_id} AND g.id = {g_id} AND uIG.user_id = u.id AND g.id = uIG.group_id;'.format(u_id=user_id, g_id=group_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getUsersInGroup(group_id):
    '''
    @brief gets the users in a group
    @param group_id the id of the group
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT user_id FROM userInGroup u WHERE u.group_id = {id} AND u.status = "Member";'.format(id=group_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getUsersNotMember(group_id):
    '''
    @brief gets the users in a group
    @param group_id the id of the group
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM user u WHERE id NOT IN (SELECT user_id from userInGroup g WHERE g.group_id = {id} AND g.status="Member");'.format(id=group_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getGroupsMemberOf(user_id):
    '''
    @brief gets the groups a user is member of
    @param user_id the id of the user
    @return returns a dict with groups
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM userInGroup u, groups g WHERE u.user_id = {id} AND u.group_id = g.id;'.format(id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getGroupsFromUser(user_id):
    '''
    @brief gets the groups a user is in
    @param user_id the id of the user
    @return returns a dict with lists
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT group_id, status FROM userInGroup u WHERE u.user_id = {id};'.format(id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getIdFromProgrammingLanguage(name):
    '''
    @brief gets the id that corresponds to a given programming language
    @param name the name of the programming_language
    @return returns an integer (the id)
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM programmingLanguage WHERE programmingLanguage.name = "{name}";'.format(name=name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getIdFromLanguage(language_code):
    '''
    @brief gets the id that corresponds to a given language
    @param name the name of the programming_language
    @return returns an integer (the id)
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM language WHERE language.language_code = "{language_code}";'.format(language_code=language_code))
    fetched = processOne(cursor)
    cursor.close()
    return fetched


def getMaxIdFromExListForUserID(user_id):
    '''

    '''
    cursor = connection.cursor()
    cursor.execute('SELECT max(e.id) AS max FROM exerciseList e WHERE e.created_by = {id};'.format(id=user_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched


def getNameFromProgLangID(ID):
    cursor = connection.cursor()
    cursor.execute('SELECT p.name FROM programmingLanguage p WHERE p.id = {id};'.format(id=ID))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllUserIDs():
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM user;')
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getAllGroupIDs():
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM groups;')
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getAllPublicGroupIDs():
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM groups WHERE group_type = 0;')
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getLastExerciseFromList(ID):
    cursor = connection.cursor()
    cursor.execute('SELECT max(exercise_number) AS last_exercise_number FROM exercise WHERE exerciseList_id = {list_id};'.format(list_id=ID))
    fetched = processOne(cursor)
    cursor.execute('SELECT max(new_list_exercise_number) AS last_exercise_number FROM exercise_references WHERE new_list_id = {list_id};'.format(list_id=ID))
    reference_fetched = processOne(cursor)
    cursor.close()

    def max_numb(f):
        if f['last_exercise_number'] is None:
            return 0
        return int(f['last_exercise_number'])

    return max(fetched, reference_fetched, key=max_numb)

def getMadeExercise(user_id, list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM madeEx WHERE user_id = {user} AND list_id = {list_id} AND exercise_number = {exercise_number};'.format(user=user_id, list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getProgrammingLanguageCodeOnName(name):
    cursor = connection.cursor()
    cursor.execute('SELECT language_code FROM programmingLanguage WHERE programmingLanguage.name = "{name}" ;'.format(name=name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getSubjectID(name):
    cursor = connection.cursor()
    cursor.execute('select id from subject WHERE name = "{name}"'.format(name=name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllSubjects():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM subject')
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getOccurenceOfSubject(subject_id):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(exerciseList_id) AS amount FROM hasSubject WHERE hasSubject.subject_id = {id};'.format(id=subject_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllSubjectIDs():
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM subject;')
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExerciseListsOnProgLang(name):
    cursor = connection.cursor()
    cursor.execute('SELECT e.id FROM exerciseList e, programmingLanguage p WHERE p.id = e.prog_lang_id AND p.name = "{name}";'.format(name=name))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getAllScoresForList(exercise_list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT madeList.score FROM madeList WHERE madeList.exerciseList_id={ex_l_id};'.format(ex_l_id=exercise_list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getAmountOfUsersWhoMadeList(exercise_list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(user_id) AS amount FROM madeList WHERE madeList.exerciseList_id = {ex_id};'.format(ex_id=exercise_list_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def averageRatingOfUsersWhoMadeList(exercise_list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT rating FROM madeList WHERE madeList.exerciseList_id = {ex_id};'.format(ex_id=exercise_list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def averageScoreForProgrammingLanguageForUser(prog_lang_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT AVG(score) AS average FROM madeList, exerciseList WHERE madeList.exerciseList_id = exerciseList.id AND exerciseList.prog_lang_id = {prog_lang_id} AND madeList.user_id = {user_id};'.format(user_id=user_id, prog_lang_id=prog_lang_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAvgScoreOfUsersWhoMadeList(exercise_list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT AVG(score) AS average FROM madeList WHERE madeList.exerciseList_id = {ex_id};'.format(ex_id=exercise_list_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllExercForUserForList(user_id, list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT mE.*,e.max_score FROM exercise e, exerciseList eL, madeEx mE WHERE eL.id = {list_id} AND e.exerciseList_id = eL.id AND mE.exercise_number = e.exercise_number AND mE.list_id = eL.id AND mE.user_id = {user_id}'.format(user_id=user_id, list_id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getAllMadeRefForUserForList(user_id, list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT mE.user_id,mE.solved,mE.exercise_score,mE.rating,mE.completed_on FROM exercise e, exerciseList eL, madeEx mE, exercise_references ref WHERE eL.id = {list_id} AND e.exerciseList_id = eL.id AND mE.exercise_number = e.exercise_number AND mE.list_id = eL.id AND mE.user_id = {user_id};'.format(user_id=user_id, list_id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getMadeListForUserForList(user_id, list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM madeList WHERE exerciseList_id = {list_id} AND user_id = {user_id};'.format(user_id=user_id, list_id=list_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getOriginalExercise(list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('SELECT original_id AS id, exercise.exercise_number AS ex_number FROM exercise_references, exercise WHERE new_list_id = {list_id} AND new_list_exercise_number = {exercise_number} AND exercise.id = original_id;'.format(list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getExerciseInList(list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM exercise WHERE exerciseList_id = {list_id} AND exercise_number = {exercise_number};'.format(list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    if fetched is None:
        return getOriginalExercise(list_id, exercise_number)
    return fetched

def getMaxSumForExForList(list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT SUM(ex.max_score) AS total FROM exercise ex WHERE ex.id = {id} ;'.format(id=list_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched['total']

def getAllListTranslations(list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT lT.name, lT.description, l.language_code FROM listTranslation lT, language l WHERE list_id = {id} AND lT.language_id = l.id ;'.format(id=list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getMaxSumForRefForList(list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT SUM(ex.max_score) AS total FROM exercise ex,exercise_references e WHERE e.new_list_id = {id} AND e.original_id = ex.id;'.format(id=list_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched['total']

def getExerciseTitle(exercise_id, language_name):
    cursor = connection.cursor()
    cursor.execute('SELECT title FROM exerciseTitle eT, language l WHERE eT.exercise_id = {id} AND l.name = "{name}" AND l.id = eT.language_id'.format(id=exercise_id, name=language_name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getExerciseQuestion(exercise_id, language_name):
    cursor = connection.cursor()
    cursor.execute('SELECT q.question_text FROM question q, language l WHERE q.exercise_id = {id} AND l.name = "{name}" AND l.id = q.language_id'.format(id=exercise_id, name=language_name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAmountOfExercisesForList(list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT GREATEST((SELECT MAX(exercise_number) FROM exercise WHERE exerciseList_id={list_id}),(SELECT MAX(new_list_exercise_number) FROM exercise_references WHERE new_list_id={list_id})) AS amount;'.format(list_id=list_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllReferencesToExercise(exercise_id):
    cursor = connection.cursor()
    cursor.execute('SELECT new_list_exercise_number AS exercise_number, new_list_id AS list_id FROM exercise_references WHERE original_id = {exercise_id} '.format(exercise_id=exercise_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getLastAnswerForExerciseForUser(user_id, list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('SELECT last_answer FROM madeEx WHERE list_id = {list_id} AND exercise_number = {exercise_number} AND user_id = {user_id}'.format(user_id=user_id, list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getScoreForExerciseForUser(user_id, list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('SELECT exercise_score FROM madeEx WHERE list_id = {list_id} AND exercise_number = {exercise_number} AND user_id = {user_id}'.format(user_id=user_id, list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getLanguageCodeForLangName(lang_name):
    cursor = connection.cursor()
    cursor.execute('SELECT language_code FROM language WHERE name = "{lang_name}" '.format(lang_name=lang_name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched["language_code"]

def getLanguageForCode(lang_code):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM language WHERE language_code = "{language_code}" '.format(language_code=lang_code))
    fetched = processOne(cursor)
    cursor.close()
    return fetched


def getLangForId(lang_id):
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM language WHERE id = {id}'.format(id=lang_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllRewards(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT b.id FROM badge b, hasBadge p WHERE b.id = p.badge_id AND p.user_id = {user_id} AND p.finished=1'.format(user_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getBadgeInformation(badge_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM badge WHERE id = {badge_id}'.format(badge_id=badge_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllBadgeInformation():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM badge')
    fetched = processData(cursor)
    cursor.close()
    return fetched

# INSERT

def insertUser(first_name, last_name, password, email, is_active, joined_on, last_login, gender):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO user(is_active,first_name,last_name,password,email,joined_on,last_login, gender) VALUES ({active},"{fname}","{lname}","{passw}","{email}", "{joined_on}", "{last_login}", "{gender}");'.format(active=is_active, fname=first_name, lname=last_name, passw=password, email=email, joined_on=joined_on, last_login=last_login, gender=gender))

def insertFriendsWith(user_id, friend_id, status):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO friendsWith(user_id,friend_id, befriended_on, status) VALUES ({u_id}, {f_id}, NOW(), "{status}");'.format(u_id=user_id, f_id=friend_id, status=status))


def insertGroup(group_name, group_type, created_on):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO groups(group_name,group_type,created_on) VALUES ("{name}", {type},"{created_on}");'.format(name=group_name, type=group_type, created_on=created_on))

def insertUserInGroup(group_id, user_id, user_permissions, joined_on, status):
    cursor = connection.cursor()
    if not userIsInGroup(user_id, group_id):
        cursor.execute('INSERT INTO userInGroup(group_id,user_id,user_permissions,joined_on, status) VALUES ({g_id}, {u_id}, {u_perm},"{joined_on}", "{status}");'.format(g_id=group_id, u_id=user_id, u_perm=user_permissions, joined_on=joined_on, status=status))

def insertProgrammingLanguage(name):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO programmingLanguage(name) VALUES ("{name}");'.format(name=name))

def insertTitleForExercise(id, language_id, title):
    cursor = connection.cursor()
    sql = 'INSERT INTO exerciseTitle(title, language_id, exercise_id) VALUES (%s, {lang_id}, {exercise_id})'.format(lang_id=language_id, exercise_id=id)
    cursor.execute(sql, [title])

def insertExercise(max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id, title, lang_id):
    cursor = connection.cursor()
    sql = 'INSERT INTO exercise(max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id) VALUES ({m},{pen},"{e_type}", {crtd_by}, "{crtd_on}", {exerc_nmbr}, {corr_answer}, {exerciseList_id});'.format(m=max_score, pen=penalty, e_type=exercise_type, crtd_by=created_by, crtd_on=created_on, exerc_nmbr=exercise_number, corr_answer=correct_answer, exerciseList_id=exerciseList_id)
    cursor.execute(sql)
    # Returns last added id (keeps on counting even through deletes?) AKA the one just added
    cursor.execute('SELECT MAX(id) AS highest_id FROM exercise WHERE exercise.created_by = {created_by};'.format(created_by=created_by))
    fetched = processOne(cursor)
    insertTitleForExercise(fetched['highest_id'], lang_id, title)
    cursor.close()
    return fetched

def insertCode(code_text, exercise_id):
    cursor = connection.cursor()
    sql = 'INSERT INTO code(code_text, exercise_id) VALUES (%s, {exerc_id});'.format(exerc_id=exercise_id)
    cursor.execute(sql, [code_text])


def insertLanguage(name):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO language(name) VALUES ("{name}");'.format(name=name))


def insertQuestion(exercise_id, language_id, question_text):
    cursor = connection.cursor()
    sql = 'INSERT INTO question(question_text,language_id,exercise_id) VALUES (%s,{l_id},{e_id});'.format(l_id=language_id, e_id=exercise_id)
    cursor.execute(sql, [question_text])


def insertAnswer(is_answer_for, language_id, answer_number, answer_text):
    cursor = connection.cursor()
    sql = 'INSERT INTO answer(answer_number,answer_text,language_id,is_answer_for) VALUES ({a_numb},%s,{l_id},{ans_for});'.format(a_numb=answer_number, l_id=language_id, ans_for=is_answer_for)
    cursor.execute(sql, [answer_text])


def insertHint(exercise_id, language_id, hint_number, hint_text):
    cursor = connection.cursor()
    sql = 'INSERT INTO hint(hint_text,hint_number,exercise_id, language_id) VALUES (%s,{h_numb},{e_id}, {lang_id});'.format(h_numb=hint_number, e_id=exercise_id, lang_id=language_id)
    cursor.execute(sql, [hint_text])

def insertListTranslation(name, description, id, lang_id):
    cursor = connection.cursor()
    sql = 'INSERT INTO listTranslation(name,description,list_id, language_id) VALUES (%s,%s,{list_id}, {lang_id});'.format(list_id=id, lang_id=lang_id)
    cursor.execute(sql, [name, description])


def insertExerciseList(name, description, difficulty, created_by, created_on, prog_lang_id, lang_id):
    cursor = connection.cursor()
    sql = 'INSERT INTO exerciseList(difficulty, created_by, created_on, prog_lang_id) VALUES ({diff}, {crtd_by}, "{crtd_on}", {prog_lang_id});'.format(diff=difficulty, crtd_by=created_by, crtd_on=created_on, prog_lang_id=prog_lang_id)
    cursor.execute(sql)
    cursor.execute('SELECT MAX(id) AS highest_id FROM exerciseList WHERE exerciseList.created_by = {created_by};'.format(created_by=created_by))
    fetched = processOne(cursor)
    insertListTranslation(name, description, fetched['highest_id'], lang_id)
    cursor.close()
    return fetched

def insertSubject(name):
    cursor = connection.cursor()
    # First check if subject is already in db
    if getSubjectID(name) is None:
        cursor.execute('INSERT INTO subject(name) VALUES ("{name}");'.format(name=name))


def insertHasSubject(exerciseList_id, subject_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO hasSubject(exerciseList_id,subject_id) VALUES ({e_id},{s_id});'.format(e_id=exerciseList_id, s_id=subject_id))


def insertMadeList(exerciseList_id, user_id, rating, score):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO madeList(exerciseList_id,user_id,rating,score, made_on, shared) VALUES ({el_id},{u_id},{rating},{score}, NOW(), 0);'.format(el_id=exerciseList_id, u_id=user_id, rating=rating, score=score))

def insertMadeExercise(user_id, solved, exercise_score, completed_on, exercise_list_id, exercise_number, last_answer, hint):
    cursor = connection.cursor()
    sql = 'INSERT INTO madeEx(user_id, solved, exercise_score,completed_on, list_id,exercise_number, last_answer, hints_used) VALUES({user},{solved},{exerc_score},"{completed_on}",{list_id},{exercise_number}, %s, {hint});'.format(user=user_id, solved=solved, exerc_score=exercise_score, completed_on=completed_on, list_id=exercise_list_id, exercise_number=exercise_number, hint=hint)
    cursor.execute(sql, [last_answer])

def insertExerciseByReference(original_exercise_id, new_list_id, new_list_exercise_number):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO exercise_references(original_id, new_list_id, new_list_exercise_number) VALUES({o_id},{l_id},{n_l_e_n});'.format(o_id=original_exercise_id, l_id=new_list_id, n_l_e_n=new_list_exercise_number))

def insertDefaultBadges(user_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO hasBadge(badge_id, user_id, current_value, finished) VALUES(25,{user_id},1,1);'.format(user_id=user_id))


# BADGES
def generateBadges():
    # Member of group

    cursor = connection.cursor()
    cursor.execute('SELECT id FROM user')
    fetched = processData(cursor)
    for member in fetched:
        checkTimeRelatedBadges(member['id'])
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('SELECT user_id FROM userInGroup')
    fetched = processData(cursor)
    for member in fetched:
        incrementBadgeValue(member['user_id'], 'memberOfGroup')
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('SELECT user_id, friend_id FROM friendsWith')
    fetched = processData(cursor)
    for user in fetched:
        incrementBadgeValue(user['user_id'], 'hasFriend')
        incrementBadgeValue(user['friend_id'], 'hasFriend')
    cursor.close()

    # solvedList
    cursor = connection.cursor()
    cursor.execute('SELECT m.user_id, l.created_by FROM madeList m, exerciseList l WHERE m.exerciseList_id = l.id')
    fetched = processData(cursor)
    for user in fetched:
        incrementBadgeValue(user['user_id'], 'solvedList')
        incrementBadgeValue(user['created_by'], 'peopleSolvedMyList')
    cursor.close()

    # createdList
    cursor = connection.cursor()
    cursor.execute('SELECT created_by FROM exerciseList')
    fetched = processData(cursor)
    for user in fetched:
        incrementBadgeValue(user['created_by'], 'createdList')
    cursor.close()

    # Write everyhting to a file
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM hasBadge')
    fetched = processData(cursor)

def changeBadge(user_id, badge_name):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM badge WHERE name ="{badge_name}"'.format(badge_name=badge_name))
    fetched = processOne(cursor)
    cursor.execute('UPDATE user SET badge_id = {badge_id} WHERE id = {user_id}'.format(badge_id=fetched['id'], user_id=user_id))
    cursor.close()

def incrementBadgeValue(user_id, badge_type):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM hasBadge g, badge b WHERE g.badge_id = b.id AND b.type = "{badge_type}" AND g.user_id = {user_id}'.format(badge_type=badge_type, user_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    cursor = connection.cursor()
    if len(fetched) > 0:
        cursor.execute('SELECT * FROM badge b, hasBadge g WHERE b.type = "{badge_type}" AND g.user_id = {user_id} AND b.id = g.badge_id'.format(user_id=user_id, badge_type=badge_type))
        data = processData(cursor)
        cursor.close()
        for element in data:
            cursor = connection.cursor()
            cursor.execute('UPDATE hasBadge SET current_value = current_value + 1 WHERE badge_id = {badge_id} AND user_id = {user_id}'.format(user_id=element['user_id'], badge_id=element['id']))
            cursor.close()

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM badge b, hasBadge g WHERE b.type = "{badge_type}" AND g.user_id = {user_id} AND b.id = g.badge_id'.format(user_id=user_id, badge_type=badge_type))
        data2 = processData(cursor)
        cursor.close()
        for element2 in data2:
            if element2['finished'] == 0:
                if element2['current_value'] >= element2['target_value']:
                    cursor = connection.cursor()
                    cursor.execute('UPDATE hasBadge SET finished = 1 WHERE badge_id = {badge_id} AND user_id = {user_id}'.format(user_id=element2['user_id'], badge_id=element2['id']))
                    cursor.close()

    else:
        cursor.execute('SELECT * FROM badge b WHERE b.type = "{badge_type}"'.format(badge_type=badge_type))
        badges_with_select_type = processData(cursor)
        cursor.close()
        for badge in badges_with_select_type:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO hasBadge(badge_id, user_id, current_value, finished) VALUES ({badge_id}, {user_id}, 1, 0)'.format(badge_id=badge['id'], user_id=user_id))
            cursor.close()

def decrementBadgeValue(user_id, badge_type):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM hasBadge g, badge b WHERE g.badge_id = b.id AND b.type = "{badge_type}" AND g.user_id = {user_id}'.format(badge_type=badge_type, user_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    cursor = connection.cursor()
    if len(fetched) > 0:
        cursor.execute('SELECT * FROM badge b, hasBadge g WHERE b.type = "{badge_type}" AND g.user_id = {user_id} AND b.id = g.badge_id'.format(user_id=user_id, badge_type=badge_type))
        data = processData(cursor)
        cursor.close()
        for element in data:
            cursor = connection.cursor()
            cursor.execute('UPDATE hasBadge SET current_value = current_value - 1 WHERE badge_id = {badge_id} AND user_id = {user_id}'.format(user_id=element['user_id'], badge_id=element['id']))
            cursor.close()

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM badge b, hasBadge g WHERE b.type = "{badge_type}" AND g.user_id = {user_id} AND b.id = g.badge_id'.format(user_id=user_id, badge_type=badge_type))
        data2 = processData(cursor)
        cursor.close()
        for element2 in data2:
            if element2['finished'] == 1:
                if element2['current_value'] < element2['target_value']:
                    cursor = connection.cursor()
                    cursor.execute('UPDATE hasBadge SET finished = 0 WHERE badge_id = {badge_id} AND user_id = {user_id}'.format(user_id=element2['user_id'], badge_id=element2['id']))
                    cursor.close()

def allBadgeEarnedUsers(badge_id):
    cursor = connection.cursor()
    cursor.execute('SELECT user_id FROM hasBadge WHERE badge_id = {badge_id} AND finished = 1'.format(badge_id=badge_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def checkTimeRelatedBadges(user_id):
    # Update Timemember
    badge_type = "timeMember"
    cursor = connection.cursor()
    cursor.execute('SELECT joined_on FROM user WHERE id ={user_id}'.format(user_id=user_id))
    fetched = processOne(cursor)
    cursor.close()

    today = time.strftime("%Y-%m-%d %H:%M:%S")
    today2 = datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
    joined_on2 = fetched['joined_on']
    naive = joined_on2.replace(tzinfo=None)

    difference = (today2 - naive).days
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM badge b WHERE b.type = "{badge_type}"'.format(badge_type=badge_type))
    data = processData(cursor)
    cursor.close()
    for badge in data:
        cursor = connection.cursor()
        cursor.execute('UPDATE hasBadge SET current_value = {dayDifference} WHERE badge_id = {badge_id} AND user_id = {user_id}'.format(dayDifference=difference, user_id=user_id, badge_id=badge['id']))
        cursor.close()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM badge b, hasBadge g WHERE b.type = "{badge_type}" AND g.user_id = {user_id} AND b.id = g.badge_id'.format(user_id=user_id, badge_type=badge_type))
        data2 = processData(cursor)
        cursor.close()
        for element2 in data2:
            if element2['finished'] == 0:
                if element2['current_value'] >= element2['target_value']:
                    cursor = connection.cursor()
                    cursor.execute('UPDATE hasBadge SET finished = 1 WHERE badge_id = {badge_id} AND user_id = {user_id}'.format(user_id=element2['user_id'], badge_id=element2['id']))
                    cursor.close()

    badge_type = "frequentVisitor"
    cursor = connection.cursor()
    cursor.execute('SELECT last_login FROM user WHERE id ={user_id}'.format(user_id=user_id))
    fetched = processOne(cursor)
    cursor.close()

    today = time.strftime("%Y-%m-%d %H:%M:%S")
    today2 = datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
    last_login2 = fetched['last_login']
    naive = joined_on2.replace(tzinfo=None)
    difference = (today2 - naive).days
    if difference == 1:
        incrementBadgeValue(user_id, "frequentVisitor")
    else:
        incrementBadgeValue(user_id, "frequentVisitor")
        resetBadgeValue(user_id, "frequentVisitor")

def getCurrentValueForBadge(badge_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT g.current_value FROM hasBadge g WHERE g.badge_id={badge_id} AND g.user_id = {user_id}'.format(user_id=user_id, badge_id=badge_id))
    fetched = processOne(cursor)
    return fetched

def resetBadgeValue(user_id, badge_type):
    cursor = connection.cursor()
    cursor.execute('UPDATE hasBadge h, badge b SET h.current_value = 1 WHERE b.type = "{badge_type}" AND h.user_id = {user_id} AND b.id = h.badge_id'.format(user_id=user_id, badge_type=badge_type))
    cursor.close()

# UPDATE

def setUserActive(email):
    cursor = connection.cursor()
    cursor.execute('UPDATE user SET is_active = 1 WHERE email = "{email}";'.format(email=email))

def updateSharedMadeExerciseList(user_id, list_id):
    cursor = connection.cursor()
    cursor.execute('UPDATE madeList SET shared = 1 WHERE exerciseList_id = {list_id} AND user_id = {user_id}'.format(list_id=list_id, user_id=user_id))

def updateUserInformation(user_id, email, password):
    cursor = connection.cursor()
    cursor.execute('UPDATE user SET email="{email}",password="{passw}" WHERE id = {id};'.format(passw=password, email=email, id=user_id))

def updateUser(user_id, first_name, last_name, password, email, is_active, permissions, joined_on, last_login, gender):
    cursor = connection.cursor()
    cursor.execute('UPDATE user SET first_name="{fname}", last_name="{lname}",is_active = "{active}",email="{email}",password="{passw}",permission="{perm}",joined_on="{joined_on}",last_login="{last_login}", gender = "{gender}" WHERE  id = {id};'.format(active=is_active, fname=first_name, lname=last_name, passw=password, email=email, id=user_id, perm=permissions, joined_on=joined_on, last_login=last_login, gender=gender))

def deleteListTranslations(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM listTranslation WHERE list_id = {list_id};'.format(list_id=id))

def updateGroup(group_id, group_name, group_type, created_on):
    cursor = connection.cursor()
    # updateGroup does not change the created_on
    cursor.execute('UPDATE groups SET group_name = "{gr_n}",group_type = {gr_t},created_on = "{created_on}" WHERE id = {id};'.format(id=group_id, gr_t=group_type, gr_n=group_name, created_on=created_on))

def updateExerciseList(list_id, name, description, difficulty, prog_lang_id, translation=None):
    cursor = connection.cursor()
    cursor.execute('UPDATE exerciseList SET prog_lang_id = {prg_id} , difficulty = {diff} WHERE id = {id};'.format(id=list_id, diff=difficulty, prg_id=prog_lang_id))
    deleteListTranslations(list_id)
    if translation:
        for key, val in translation.items():
            if len(val):
                insertListTranslation(val['name'], val['description'], list_id, key.id)

def updateListRating(list_id, user_id, list_rating):
    cursor = connection.cursor()
    cursor.execute('UPDATE madeList SET rating = {rating} WHERE exerciseList_id = {list_id} AND user_id = {user_id}'.format(rating=list_rating, list_id=list_id, user_id=user_id))

def UpdateExerciseAndReferenceNumbers(sql_string):
    cursor = connection.cursor()
    cursor.execute('START TRANSACTION;' + sql_string + 'COMMIT;')

def updateExerciseCode(code, exercise_id):
    cursor = connection.cursor()
    sql = 'UPDATE code SET code_text = %s WHERE exercise_id = {exercise_id}'.format(exercise_id=exercise_id)
    cursor.execute(sql, [code])

def updateQuestion(ex_id, lang_id, question_text):
    question = getExerciseQuestion(ex_id, getLangForId(lang_id)['name'])
    if question:
        cursor = connection.cursor()
        sql = 'UPDATE question SET question_text = %s WHERE exercise_id = {ex_id} AND language_id={lang_id};'.format(ex_id=ex_id, lang_id=lang_id)
        cursor.execute(sql, [question_text])
    else:
        insertQuestion(ex_id, lang_id, question_text)

def updateFriendship(user_id, friend_id):
    '''
    @brief confirms a friendship, changes status
    @param id the id of the user, id of the friend that will be acceptes
    @return returns nothing
    '''
    cursor = connection.cursor()
    cursor.execute('UPDATE friendsWith SET status="Friends" WHERE user_id = {friend_id} AND friend_id = {user_id};'.format(user_id=user_id, friend_id=friend_id))

def updateGroupMembership(user_id, group_id):
    '''
    @brief confirms group membership, changes status
    @param id the id of the user, id of group
    @return returns nothing
    '''
    cursor = connection.cursor()
    cursor.execute('UPDATE userInGroup SET status="Member" WHERE user_id = {user_id} AND group_id = {group_id};'.format(user_id=user_id, group_id=group_id))

def updateUserPermissions(group_id, user_id, permission_level):
    '''
    @brief upgrade group permissions
    @param id the id of the user, id of group and the new permission level
    @return returns nothing
    '''
    cursor = connection.cursor()
    cursor.execute('UPDATE userInGroup SET user_permissions={permission_level} WHERE user_id = {user_id} AND group_id = {group_id};'.format(user_id=user_id, group_id=group_id, permission_level=permission_level))

def updateExerciseTitle(exercise_id, lang_id, new_title):
    title = getExerciseTitle(exercise_id, getLangForId(lang_id)['name'])
    if title:
        cursor = connection.cursor()
        sql = 'UPDATE exerciseTitle SET title=%s WHERE exercise_id = {exercise_id} AND language_id = {lang_id};'.format(exercise_id=exercise_id, lang_id=lang_id)
        cursor.execute(sql, [new_title])
    else:
        insertTitleForExercise(exercise_id, lang_id, new_title)

def updateExerciseAnswer(exercise_id, lang_id, answer_number, answer_text):
    cursor = connection.cursor()
    sql = 'UPDATE answer SET answer_text=%s WHERE exercise_id = {id} AND language_id = {lang_id} AND answer_number = {answer_number}'.format(id=exercise_id, lang_id=lang_id, answer_number=answer_number)
    cursor.execute(sql, [answer_text])

def updateExerciseHint(exercise_id, lang_id, hints_number, hint_text):
    cursor = connection.cursor()
    sql = 'UPDATE hint SET hint_text=%s WHERE exercise_id = {id} AND language_id = {lang_id} AND hint_number = {hint_number}'.format(id=exercise_id, lang_id=lang_id, hint_number=hints_number)
    cursor.execute(sql, [hint_text])

def updateExercise(exercise_id, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id, title, language_id):
    cursor = connection.cursor()
    cursor.execute('UPDATE exercise SET max_score={max_score},penalty={penalty},created_by={created_by},created_on="{created_on}",exercise_number={exercise_number},correct_answer={correct_answer},exerciseList_id={exerciseList_id} WHERE id = {exercise_id} ;'.format(exercise_id=exercise_id, max_score=max_score, penalty=penalty, exercise_type=exercise_type, created_by=created_by, created_on=created_on, exercise_number=exercise_number, correct_answer=correct_answer, exerciseList_id=exerciseList_id))
    updateExerciseTitle(exercise_id, language_id, title)

def updateMadeExercise(list_id, user_id, exercise_number, answer, solved, completed_on, hint, exercise_score):
    cursor = connection.cursor()
    sql = 'UPDATE madeEx SET last_answer=%s, solved={solved}, completed_on="{completed_on}", hints_used={hint}, exercise_score={exercise_score} WHERE user_id = {user_id} AND exercise_number = {exercise_number} AND list_id={list_id};'.format(user_id=user_id, exercise_number=exercise_number, list_id=list_id, answer=answer, solved=solved, completed_on=completed_on, hint=hint, exercise_score=exercise_score)
    cursor.execute(sql, [answer])

# DELETE

def deleteGroup(group_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM userInGroup WHERE group_id={group_id};'.format(group_id=group_id))
    cursor.execute('DELETE FROM groups WHERE id={group_id};'.format(group_id=group_id))

def deleteFriendship(user_id, friend_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM friendsWith WHERE user_id = {friend_id} AND friend_id = {user_id};'.format(user_id=user_id, friend_id=friend_id))
    cursor.execute('DELETE FROM friendsWith WHERE user_id = {user_id} AND friend_id = {friend_id};'.format(user_id=user_id, friend_id=friend_id))

def deleteGroupMembership(user_id, group_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM userInGroup WHERE user_id = {user_id} AND group_id = {group_id};'.format(user_id=user_id, group_id=group_id))

def deleteUserFromGroup(group_id, user_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM userInGroup WHERE user_id = {user_id} AND group_id = {group_id};'.format(user_id=user_id, group_id=group_id))

def deleteHints(exercise_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM hint WHERE hint.exercise_id={id};'.format(id=exercise_id))

def deleteAnswers(exercise_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM answer WHERE answer.is_answer_for={id};'.format(id=exercise_id))

def deleteExercise(exercise_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM hint WHERE exercise_id={id};'.format(id=exercise_id))
    cursor.execute('DELETE FROM question WHERE exercise_id={id};'.format(id=exercise_id))
    cursor.execute('DELETE FROM code WHERE exercise_id={id};'.format(id=exercise_id))
    cursor.execute('DELETE FROM answer WHERE is_answer_for={id};'.format(id=exercise_id))
    cursor.execute('DELETE FROM exerciseTitle WHERE exercise_id={id}'.format(id=exercise_id))
    cursor.execute('DELETE FROM exercise WHERE id={id};'.format(id=exercise_id))

def deleteSubjectFromHasSubject(list_id, subject_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM hasSubject WHERE exerciseList_id = {list_id} AND subject_id = {subject_id}'.format(subject_id=subject_id, list_id=list_id))

def deleteReference(list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM exercise_references WHERE new_list_id = {list_id} AND new_list_exercise_number = {new_list_exercise_number}'.format(new_list_exercise_number=exercise_number, list_id=list_id))

# TRIVIA

def hasUserSolvedExercise(list_id, exercise_number, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT solved FROM madeEx WHERE list_id = {list_id} AND exercise_number = {exercise_number} AND user_id = {user_id}'.format(user_id=user_id, list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def userIsInGroup(user_id, group_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user u, userInGroup uIG WHERE u.id = {user_id} AND uIG.group_id = {group_id} AND u.id = uIG.user_id;'.format(user_id=user_id, group_id=group_id))
    fetched = processOne(cursor)
    cursor.close()
    if fetched is None:
        return False
    return True

def countExerciseListsForProgrammingLanguageID(prog_lang_id):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(id) AS amount FROM exerciseList WHERE exerciseList.prog_lang_id = {id} ;'.format(id=prog_lang_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def countExerciseListsForProgrammingLanguageIDMadeByUser(prog_lang_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(exerciseList_id) AS amount FROM madeList, exerciseList WHERE exerciseList.prog_lang_id = {id} AND exerciseList.id = madeList.exerciseList_id AND madeList.user_id = {user_id};'.format(id=prog_lang_id, user_id=user_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def countExercisesForProgrammingLanguageIDMadeByUser(prog_lang_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(madeEx.solved) AS amount FROM madeEx, exerciseList, exercise WHERE exerciseList.prog_lang_id = {id} AND exerciseList.id = madeEx.list_id AND madeEx.user_id = {user_id} AND madeEx.solved = 1 AND madeEx.list_id = exercise.exerciseList_id AND madeEx.exercise_number = exercise.exercise_number ;'.format(id=prog_lang_id, user_id=user_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def latestAnswer(exercise_id, language_id):
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(answer_number) AS highest FROM answer WHERE answer.language_id = {l_id} AND answer.is_answer_for = {ex_id};'.format(l_id=language_id, ex_id=exercise_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def latestHint(exercise_id, language_code):
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(answer_number) AS highest FROM hint WHERE hint.language_id = {l_id} AND hint.exercise_id = {ex_id};'.format(l_id=language_id, ex_id=exercise_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def latestHintUserUsedForExercise(list_id, exercise_number, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT hints_used FROM madeEx WHERE list_id = {list_id} AND exercise_number = {exercise_number} AND user_id = {user_id}'.format(user_id=user_id, list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def userUsesHint(list_id, exercise_number, user_id, new_latest, current_score):
    cursor = connection.cursor()
    cursor.execute('UPDATE madeEx SET hints_used = {new_latest}, exercise_score = {exercise_score} WHERE user_id = {user_id} AND exercise_number={exercise_number} AND list_id={list_id};'.format(user_id=user_id, exercise_number=exercise_number, list_id=list_id, new_latest=new_latest, exercise_score=current_score))

def userIsWorkingOn(list_id, exercise_number, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM madeEx WHERE list_id = {list_id} AND exercise_number = {exercise_number} AND user_id = {user_id}'.format(user_id=user_id, list_id=list_id, exercise_number=exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def amountOfListsWithSubjectForUser(subject_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(madeList.exerciseList_id) AS amount FROM hasSubject,madeList WHERE hasSubject.subject_id = {sub_id} AND hasSubject.exerciseList_id = madeList.exerciseList_id AND madeList.user_id={u_id};'.format(sub_id=subject_id, u_id=user_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def amountOfListsWithProgrammingLanguageForUser(prog_lang, id):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(exerciseList.id) AS amount FROM exerciseList,madeList WHERE exerciseList.prog_lang_id = {prog_id} AND exerciseList.id = madeList.exerciseList_id AND madeList.user_id={u_id};'.format(prog_id=prog_lang, u_id=id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def listOfRatingsForUser(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT rating FROM madeList WHERE madeList.user_id={u_id};'.format(u_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def listOfRatingsForUserForSubject(user_id, subject_id):
    cursor = connection.cursor()
    cursor.execute('SELECT rating FROM hasSubject,madeList WHERE hasSubject.subject_id = {id} AND hasSubject.exerciseList_id = madeList.exerciseList_id AND madeList.user_id={u_id};'.format(id=subject_id, u_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def listOfRatingsForUserForProgrammingLanguage(user_id, prog_lang_id):
    cursor = connection.cursor()
    cursor.execute('SELECT rating FROM exerciseList,madeList WHERE exerciseList.prog_lang_id = {id} AND exerciseList.id = madeList.exerciseList_id AND madeList.user_id={u_id};'.format(id=prog_lang_id, u_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def listOfDatesForUser(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT made_on FROM madeList WHERE madeList.user_id={u_id};'.format(u_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def listOfDatesForUserForSubject(user_id, subject_id):
    cursor = connection.cursor()
    cursor.execute('SELECT made_on FROM hasSubject,madeList WHERE hasSubject.subject_id = {id} AND hasSubject.exerciseList_id = madeList.exerciseList_id AND madeList.user_id={u_id};'.format(id=subject_id, u_id=user_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def listOfDatesForUserForProgrammingLanguage(id, prog_lang_id):
    cursor = connection.cursor()
    cursor.execute('SELECT made_on FROM exerciseList,madeList WHERE exerciseList.prog_lang_id = {id} AND exerciseList.id = madeList.exerciseList_id AND madeList.user_id={u_id};'.format(id=prog_lang_id, u_id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched


def copyExercise(original_exercise_id, exercise_number, new_exercise_list_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO exercise(max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id) SELECT max_score, penalty, exercise_type, created_by, created_on, {exercise_number} AS exercise_number, correct_answer, {list_id} AS exerciseList_id FROM exercise WHERE id = {id};'.format(id=original_exercise_id, exercise_number=exercise_number, list_id=new_exercise_list_id))
    # Returns last added id (keeps on counting even through deletes?) AKA the one just added
    cursor.execute('SELECT MAX(id) AS highest_id FROM exercise;')
    new_id = processOne(cursor)['highest_id']
    # Copy the information
    cursor.execute('INSERT INTO exerciseTitle(title, exercise_id, language_id) SELECT title, {new_id} AS exercise_id, language_id FROM exerciseTitle WHERE exercise_id = {id}'.format(id=original_exercise_id, new_id=new_id))

    cursor.execute('INSERT INTO answer(answer_number, answer_text, language_id, is_answer_for) SELECT answer_number, answer_text, language_id, {id} AS is_answer_for FROM answer WHERE is_answer_for = {or_id};'.format(id=new_id, or_id=original_exercise_id))
    cursor.execute('INSERT INTO hint(hint_text, hint_number, exercise_id, language_id) SELECT hint_text, hint_number,{id} AS exercise_id, language_id FROM hint WHERE exercise_id = {or_id};'.format(id=new_id, or_id=original_exercise_id))
    cursor.execute('INSERT INTO code(code_text, exercise_id) SELECT code_text, {id} AS exercise_id FROM code WHERE exercise_id = {or_id};'.format(id=new_id, or_id=original_exercise_id))
    cursor.execute('INSERT INTO question(question_text, language_id, exercise_id) SELECT question_text, language_id, {id} AS exercise_id FROM question WHERE exercise_id = {or_id};'.format(id=new_id, or_id=original_exercise_id))

    cursor.close()
    return new_id

def isReference(list_id, exercise_number):
    original = getOriginalExercise(list_id, exercise_number)
    if original:
        return True
    else:
        return False

def allExerciseListIDs():
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM exerciseList;')
    fetched = processData(cursor)
    cursor.close()
    return fetched

# USER VERIFICATION
def needsVerification(hash):
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM verification WHERE hash = "{hash}";'.format(hash=hash))
    result = processOne(cursor)
    cursor.close()
    if result:
        return result['email']
    else:
        return None

def addVerification(email, hash):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO verification(email, hash) VALUES ("{email}","{hash}");'.format(email=email, hash=hash))


# Filtering
def filterOn(list_name, min_list_difficulty, max_list_difficulty, user_first_name, user_last_name, prog_lang_name, subject_name, order_mode, lang_id):
    cursor = connection.cursor()
    subject_search = ""
    if isinstance(subject_name, list):
        subs = ""
        if len(subject_name) > 1:
            for i, s in enumerate(subject_name):
                if i == len(subject_name) - 1:
                    subs += '"' + s + '"'
                else:
                    subs += '"' + s + '"' + ','
            subject_search = 'IN ({subject})'.format(subject=subs)
        else:
            subject_search = 'LIKE "%{subject}%"'.format(subject=subject_name[0])

    else:
        subject_search = 'LIKE "%{subject}%"'.format(subject=subject_name)

    cursor.execute(' SELECT DISTINCT e.*, lT.name, lT.description, lT.language_id , COUNT(mL.exerciseList_id) * (AVG(mL.rating) / 5) as popularity FROM (exerciseList e, programmingLanguage pL, user u, listTranslation lT) '
                   ' LEFT JOIN hasSubject h ON e.id = h.exerciseList_id'
                   ' LEFT JOIN madeList mL ON e.id = mL.exerciseList_id '
                   ' LEFT JOIN subject s ON e.id = h.exerciseList_id AND h.subject_id = s.id'
                   ' WHERE s.name {subject} AND lT.name LIKE "%{name}%" AND u.id = e.created_by AND u.first_name LIKE "%{first_name}%" '
                   ' AND u.last_name LIKE "%{last_name}%"'
                   ' AND pL.id = e.prog_lang_id AND pL.name LIKE "{prog_lang}"'
                   ' AND e.difficulty <= {max_diff} AND e.difficulty >= {min_diff}'
                   ' AND lT.list_id = e.id AND (lT.language_id = {lang_id} OR lT.language_id = 1)'
                   ' GROUP BY lT.name ORDER BY popularity {order_mode};'
                   .format(name=list_name, min_diff=min_list_difficulty, max_diff=max_list_difficulty, first_name=user_first_name, last_name=user_last_name,
                           prog_lang=prog_lang_name, subject=subject_search, order_mode=order_mode, lang_id=lang_id))
    fetched = processData(cursor)

    cursor.close()
    # Clear doubles/ if any
    if lang_id != 1:
        info = {}
        for i in fetched:
            if i['id'] not in info.keys():
                info[i['id']] = 1
            else:
                info[i['id']] += 1

        cleaned = []
        for i in fetched:
            if info[i['id']] == 1:
                cleaned.append(i)
            else:
                if int(i['language_id']) != 1:
                    cleaned.append(i)

        return cleaned

    return fetched


def filterLists(name):
    cursor = connection.cursor()
    cursor.execute('select DISTINCT eL.* from exercise e, exerciseList eL WHERE e.title LIKE "%{name}%" OR eL.name LIKE "%{name}%";'.format(name=name))
    fetched = processData(cursor)
    cursor.close()
    return fetched

# Post table

def insertPost(group_id, user_id, reply, reply_number, post_text, posted_on):
    cursor = connection.cursor()
    sql = 'INSERT INTO post(group_id, user_id, reply, reply_number, post_text, posted_on) VALUES ({group_id}, {user_id}, {reply}, {reply_number}, %s, "{posted_on}");'.format(group_id=group_id, user_id=user_id, reply=reply, reply_number=reply_number, posted_on=posted_on)
    cursor.execute(sql, [post_text])

def lastPostID():
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(id) AS last FROM post;')
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def lastReplyToPost(post_id):
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(reply_number) AS last FROM post WHERE id={post_id};'.format(post_id=post_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def updatePost(post_id, text):
    cursor = connection.cursor()
    sql = 'UPDATE post SET post_text=%s WHERE id={post_id};'.format(post_id=post_id)
    cursor.execute(sql, [text])

def deletePost(post_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM post WHERE id = {post_id};'.format(post_id=post_id))

def getAllPostsForGroup(group_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM post WHERE group_id={group_id};'.format(group_id=group_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched


# Challenges

def createChallenge(challenger_id, challenged_id, challenge_type, challenge_list_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO challenge(challenger_id, challenged_id, list_id, challenge_type_id, status) VALUES ({challenger}, {challenged_id}, {list}, {challenge_type_id}, "Pending");'.format(challenger=challenger_id, challenged_id=challenged_id, list=challenge_list_id, challenge_type_id=challenge_type))
    cursor.close()

def getChallengeForStatus(user_id, status):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM challenge WHERE status="{status}" AND (challenged_id = {user} OR challenger_id = {user})'.format(user=user_id, status=status))
    fetched = processData(cursor)
    cursor.close()
    return fetched


def cancelChallenge(challenger_id, challenged_id, challenge_list_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM challenge WHERE challenger_id = {challenger} AND challenged_id = {challenged_id} AND list_id = {list};'.format(challenger=challenger_id, challenged_id=challenged_id, list=challenge_list_id))
    cursor.close()


def acceptChallenge(challenger_id, challenged_id, challenge_list_id):
    cursor = connection.cursor()
    cursor.execute('UPDATE challenge SET status="Accepted" WHERE challenger_id = {challenger} AND challenged_id = {challenged_id} AND list_id = {list};'.format(challenger=challenger_id, challenged_id=challenged_id, list=challenge_list_id))
    cursor.close()

def finishChallenge(challenger_id, challenged_id, challenge_list_id, winner_id):
    cursor = connection.cursor()
    cursor.execute('UPDATE challenge SET status="Finished", winner_id = {winner_id} WHERE challenger_id = {challenger} AND challenged_id = {challenged_id} AND list_id = {list};'.format(challenger=challenger_id, challenged_id=challenged_id, list=challenge_list_id, winner_id=winner_id))
    cursor.close()

def getChallengesBetween(challenger_id, challenged_id):
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT * FROM challenge WHERE (challenger_id = {user} OR challenged_id = {user}) AND (challenger_id = {challenged} OR challenged_id = {challenged})'.format(user=challenger_id, challenged=challenged_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched


def getAllRepliesToPost(post_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM post WHERE reply={post_id};'.format(post_id=post_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getChallengeWinsAgainst(user_id, opponent_id):
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT * FROM challenge WHERE (challenger_id = {user} OR challenged_id = {user}) AND (challenger_id = {challenged} OR challenged_id = {challenged}) AND winner_id = {user}'.format(user=user_id, challenged=opponent_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getFinishedChallengesBetween(user_id, opponent_id):
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT * FROM challenge WHERE (challenger_id = {user} OR challenged_id = {user}) AND (challenger_id = {challenged} OR challenged_id = {challenged}) AND status = "Finished"'.format(user=user_id, challenged=opponent_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

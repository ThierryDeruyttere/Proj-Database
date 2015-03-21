from django.db import connection

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
    if(len(dictfetchall(cursor)) > 0):
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

def getExerciseListInformation(id):
    '''
    @brief get the information from Exercise lists given an user id
    @param id the id of the user
    @return returns a dict with information
    '''
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM exerciseList WHERE id = {id};'.format(id=id))
    fetched = processOne(cursor)
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
    if(exercise_type == "Open Question"):
        cursor.execute('SELECT e.*, "" AS code_text, q.question_text, p.name AS programming_language, l.name AS language_name FROM programmingLanguage p, exerciseList eL, exercise e, language l, question q WHERE e.id = {id} AND e.id = q.exercise_id AND q.language_id = l.id AND e.exerciseList_id = eL.id AND eL.prog_lang_id = p.id  AND l.language_code = "{lang_name}";'.format(id=id, lang_name=language_code))
    else:
        cursor.execute('SELECT e.*, c.code_text, q.question_text, p.name AS programming_language, l.name AS language_name FROM programmingLanguage p, exerciseList eL, code c, exercise e, language l, question q WHERE e.id = {id} AND e.id = c.exercise_id  AND e.id = q.exercise_id AND q.language_id = l.id AND e.exerciseList_id = eL.id AND eL.prog_lang_id = p.id  AND l.language_code = "{lang_name}";'.format(id=id, lang_name=language_code))
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
    cursor.execute('SELECT f.friend_id FROM friendsWith f WHERE f.user_id = {id} UNION SELECT f.user_id FROM friendsWith f WHERE f.friend_id = {id};'.format(id=id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getFriendsNotMemberOfGroupWithID(me_id, group_id):
    cursor = connection.cursor()
    print('SELECT DISTINCT u2.id FROM user u, user u2, friendsWith fW, userInGroup uIG, groups g WHERE g.id = {group_id} AND u.id = {me_id} AND u.id <> u2.id AND u2.id <> uIG.user_id AND uIG.group_id = g.id AND ((u.id = fW.user_id AND u2.id = fW.friend_id) OR (u2.id = fW.user_id AND u.id = fW.friend_id));'.format(me_id=me_id, group_id=group_id))
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

def getProgrammingLanguageIDsOfMadeExForUser(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT l.prog_lang_id FROM user u,exercise e, madeEx m, exerciseList l WHERE  u.id = {id} AND u.id = m.user_id AND m.exercise_id = e.id AND e.exerciseList_id = l.id AND solved = 1;'.format(id = user_id))
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
    cursor.execute('SELECT mE.exercise_id, mE.solved, mE.exercise_score, mE.rating,mE.completed_on FROM user u, exerciseList eL, madeEx mE, exercise e WHERE u.id = {u_id} AND eL.id = {el_id} AND e.exerciseList_id = eL.id AND e.id =  mE.exercise_id AND mE.user_id = u.id;'.format(u_id=id, el_id=exercise_list))
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
    cursor.execute('SELECT user_id FROM userInGroup u WHERE u.group_id = {id};'.format(id=group_id))
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
    cursor.execute('SELECT group_id FROM userInGroup u WHERE u.user_id = {id};'.format(id=user_id))
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
    cursor.close()
    return fetched

def getMadeExercise(user_id, exercise_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM madeEx WHERE user_id = {user} AND exercise_id = {exerc};'.format(user = user_id, exerc = exercise_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getProgrammingLanguageCodeOnName(name):
    cursor = connection.cursor()
    cursor.execute('SELECT language_code FROM programmingLanguage WHERE programmingLanguage.name = "{name}" ;'.format(name = name))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getSubjectID(name):
    cursor = connection.cursor()
    cursor.execute('select id from subject WHERE name = "{name}"'.format(name = name))
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
    cursor.execute('SELECT COUNT(exerciseList_id) AS amount FROM hasSubject WHERE hasSubject.subject_id = {id};'.format(id = subject_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getAllSubjectIDs():
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM subject;')
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getExerciseListsOnProgLang(progLang):
    cursor = connection.cursor()
    cursor.execute('SELECT e.id FROM exerciseList e, programmingLanguage p WHERE p.id = e.prog_lang_id AND p.name = "{name}";'.format(name=progLang))
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
    cursor.execute('SELECT AVG(rating) AS average FROM madeList WHERE madeList.exerciseList_id = {ex_id};'.format(ex_id=exercise_list_id))
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
    cursor.execute('SELECT * FROM exercise e, exerciseList eL, madeEx mE WHERE eL.id = {list_id} AND e.exerciseList_id = eL.id AND mE.exercise_id = e.id AND mE.user_id = {user_id}'.format(user_id=user_id, list_id = list_id))
    fetched = processData(cursor)
    cursor.close()
    return fetched

def getMadeListForUserForList(user_id, list_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM madeList WHERE exerciseList_id = {list_id} AND user_id = {user_id}'.format(user_id=user_id, list_id = list_id))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def getOriginalExercise(list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('SELECT original_id FROM exercise_references WHERE new_list_id = {list_id} AND new_list_exercise_number = {exercise_number}'.format(list_id=list_id, exercise_number = exercise_number))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

##INSERT
def insertUser(first_name, last_name, password, email, is_active, joined_on, last_login, gender):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO user(is_active,first_name,last_name,password,email) VALUES ({active},"{fname}","{lname}","{passw}","{email}");'.format(active=is_active, fname=first_name, lname=last_name, passw=password, email=email))


def insertFriendsWith(user_id, friend_id, status):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO friendsWith(user_id,friend_id, befriended_on, status) VALUES ({u_id}, {f_id}, CURDATE(), "{status}");'.format(u_id=user_id, f_id=friend_id, status=status))


def insertGroup(group_name, group_type, created_on):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO groups(group_name,group_type,created_on) VALUES ("{name}", {type},"{created_on}");'.format(name=group_name, type=group_type, created_on=created_on))

def insertUserInGroup(group_id, user_id, user_permissions, joined_on):
    cursor = connection.cursor()
    if not userIsInGroup(user_id, group_id):
        cursor.execute('INSERT INTO userInGroup(group_id,user_id,user_permissions,joined_on) VALUES ({g_id}, {u_id}, {u_perm},"{joined_on}");'.format(g_id=group_id, u_id=user_id, u_perm=user_permissions, joined_on=joined_on))


def insertProgrammingLanguage(name):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO programmingLanguage(name) VALUES ("{name}");'.format(name=name))

def insertExercise(difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id, title):
    cursor = connection.cursor()
    sql = 'INSERT INTO exercise(difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id, title) VALUES ({diff},{m},{pen},"{e_type}", {crtd_by}, "{crtd_on}", {exerc_nmbr}, {corr_answer}, {exerciseList_id}, %s);'.format(diff=difficulty, m=max_score, pen=penalty, e_type=exercise_type, crtd_by=created_by, crtd_on=created_on, exerc_nmbr=exercise_number, corr_answer=correct_answer, exerciseList_id=exerciseList_id)

    cursor.execute(sql, [title])
    # Returns last added id (keeps on counting even through deletes?) AKA the one just added
    cursor.execute('SELECT MAX(id) AS highest_id FROM exercise WHERE exercise.created_by = {created_by};'.format(created_by=created_by))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def insertCode(code_text, exercise_id):
    cursor = connection.cursor()
    sql = 'INSERT INTO code(code_text, exercise_id) VALUES (%s, {exerc_id});'.format(exerc_id=exercise_id)
    cursor.execute(sql, [code_text])


def insertLanguage(name):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO language(name) VALUES ("{name}");'.format(name=name))


def insertQuestion(question_text, language_id, exercise_id):
    cursor = connection.cursor()
    sql = 'INSERT INTO question(question_text,language_id,exercise_id) VALUES (%s,{l_id},{e_id});'.format(l_id=language_id, e_id=exercise_id)
    cursor.execute(sql, [question_text])


def insertAnswer(answer_number, answer_text, language_id, is_answer_for):
    cursor = connection.cursor()
    sql = 'INSERT INTO answer(answer_number,answer_text,language_id,is_answer_for) VALUES ({a_numb},%s,{l_id},{ans_for});'.format(a_numb=answer_number, l_id=language_id, ans_for=is_answer_for)
    cursor.execute(sql, [answer_text])


def insertHint(hint_text, hint_number, exercise_id, language_id):
    cursor = connection.cursor()
    sql = 'INSERT INTO hint(hint_text,hint_number,exercise_id, language_id) VALUES (%s,{h_numb},{e_id}, {lang_id});'.format(h_numb=hint_number, e_id=exercise_id, lang_id=language_id)
    cursor.execute(sql, [hint_text])


def insertExerciseList(name, description, difficulty, created_by, created_on, prog_lang_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO exerciseList(name,description,difficulty, created_by, created_on, prog_lang_id) VALUES ("{name}","{desc}",{diff}, {crtd_by}, "{crtd_on}", {prog_lang_id});'.format(name=name, desc=description, diff=difficulty, crtd_by=created_by, crtd_on=created_on, prog_lang_id=prog_lang_id))
    cursor.execute('SELECT MAX(id) AS highest_id FROM exerciseList WHERE exerciseList.created_by = {created_by};'.format(created_by=created_by))
    fetched = processOne(cursor)
    cursor.close()
    return fetched

def insertSubject(name):
    cursor = connection.cursor()
    # First check if subject is already in db
    if(getSubjectID(name) is None):
        cursor.execute('INSERT INTO subject(name) VALUES ("{name}");'.format(name=name))


def insertHasSubject(exerciseList_id, subject_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO hasSubject(exerciseList_id,subject_id) VALUES ({e_id},{s_id});'.format(e_id=exerciseList_id, s_id=subject_id))


def insertMadeList(exerciseList_id, user_id, rating, score):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO madeList(exerciseList_id,user_id,rating,score, made_on) VALUES ({el_id},{u_id},{rating},{score}, CURDATE());'.format(el_id=exerciseList_id, u_id=user_id, rating=rating, score=score))

def insertMadeExercise(user_id, exercise_id, solved, exercise_score, rating, completed_on, exercise_list_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO madeEx(user_id, exercise_id, solved, exercise_score, rating,completed_on, list_id) VALUES({user},{ex_id},{solved},{exerc_score},{rating},"{completed_on}",{list_id});'.format(user=user_id, ex_id=exercise_id, solved=solved, exerc_score=exercise_score, rating=rating, completed_on=completed_on, list_id=exercise_list_id))

def insertExerciseByReference(original_exercise_id, new_list_id, new_list_exercise_number):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO exercise_references(original_id, new_list_id, new_list_exercise_number) VALUES({o_id},{l_id},{n_l_e_n});'.format(o_id=original_exercise_id, l_id=new_list_id, n_l_e_n=new_list_exercise_number))

# UPDATE

def updateUserInformation(user_id, email, password):
    cursor = connection.cursor()
    cursor.execute('UPDATE user SET email="{email}",password="{passw}" WHERE id = {id};'.format(passw=password, email=email, id=user_id))


def updateUser(user_id, first_name, last_name, password, email, is_active, permissions, joined_on, last_login, gender):
    cursor = connection.cursor()
    cursor.execute('UPDATE user SET first_name="{fname}", last_name="{lname}",is_active = {active},email="{email}",password="{passw}",permission = {perm},joined_on="{joined_on}",last_login="{last_login}", gender = "{gender}" WHERE  id = {id};'.format(active=is_active, fname=first_name, lname=last_name, passw=password, email=email, id=user_id, perm=permissions, joined_on=joined_on, last_login=last_login, gender=gender))


def updateGroup(group_id, group_name, group_type, created_on):
    cursor = connection.cursor()
    # updateGroup does not change the created_on
    cursor.execute('UPDATE groups SET group_name = "{gr_n}",group_type = {gr_t},created_on = "{created_on}" WHERE id = {id};'.format(id=group_id, gr_t=group_type, gr_n=group_name, created_on=created_on))


def updateExerciseList(list_id, name, description, difficulty, prog_lang_id):
    cursor = connection.cursor()
    cursor.execute('UPDATE exerciseList SET description = "{desc}",name = "{name}", prog_lang_id = {prg_id} , difficulty = {diff} WHERE id = {id};'.format(id=list_id, desc=description, name=name, diff=difficulty, prg_id=prog_lang_id))

def updateListRating(list_id, user_id, list_rating):
    cursor = connection.cursor()
    cursor.execute('UPDATE madeList SET rating = {rating} WHERE exerciseList_id = {list_id} AND user_id = {user_id}'.format(rating = list_rating, list_id = list_id, user_id = user_id))


def updateExercise(exercise_id, difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id):
    print(created_on)
    cursor = connection.cursor()
    cursor.execute('UPDATE exercise SET difficulty = {diff}, max_score = {m}, penalty = {pen}, exercise_type = "{e_type}", created_by = {crtd_by}, created_on = "{crtd_on}", exercise_number = {exerc_nmbr}, correct_answer = {corr_answer}, exerciseList_id = {exerciseList_id} WHERE id = {ex_id};'.format(ex_id=exercise_id, diff=difficulty, m=max_score, pen=penalty, e_type=exercise_type, crtd_by=created_by, crtd_on=created_on, exerc_nmbr=exercise_number, corr_answer=correct_answer, exerciseList_id=exerciseList_id))


def updateFriendship(user_id, friend_id):
    '''
    @brief confirms a friendship, changes status
    @param id the id of the user, id of the friend that will be acceptes
    @return returns nothing
    '''
    cursor = connection.cursor()
    cursor.execute('UPDATE friendsWith SET status="Friends" WHERE user_id = {friend_id} AND friend_id = {user_id};'.format(user_id=user_id, friend_id=friend_id))

# DELETE

def deleteAnswers(exercise_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM answer WHERE answer.is_answer_for={id};'.format(id=exercise_id))


def deleteHints(hint_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM hint WHERE hint.exercise_id={id};'.format(id=hint_id))


def deleteSubjectFromHasSubject(list_id, subject_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM hasSubject WHERE exerciseList_id = {list_id} AND subject_id = {subject_id}'.format(subject_id=subject_id, list_id=list_id))

def deleteReference(list_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM exercise_references WHERE new_list_id = {list_id} AND new_list_exercise_number = {new_list_exercise_number}'.format(new_list_exercise_number=exercise_number, list_id=list_id))

# TRIVIA

def userIsInGroup(user_id, group_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user u, userInGroup uIG WHERE u.id = {user_id} AND uIG.group_id = {group_id} AND u.id = uIG.user_id;'.format(user_id = user_id, group_id=group_id))
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

def copyExercise(original_exercise_id, exercise_number):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO exercise(difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id, title) SELECT difficulty, max_score, penalty, exercise_type, created_by, created_on, {exercise_number} AS exercise_number, correct_answer, exerciseList_id, title FROM exercise WHERE id = {id};'.format(id=original_exercise_id, exercise_number=exercise_number))

    # Returns last added id (keeps on counting even through deletes?) AKA the one just added
    cursor.execute('SELECT MAX(id) AS highest_id FROM exercise;')
    new_id = processOne(cursor)['highest_id']
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

def removeVerification(hash):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM verification WHERE hash = "{hash}";'.format(hash=hash))


def addVerification(email, hash):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO verification(email, hash) VALUES ("{email}","{hash}");'.format(email=email, hash=hash))


#Filtering
def filterOn(list_name, min_list_difficulty, max_list_difficulty, user_first_name, user_last_name, prog_lang_name, subject_name, order_mode):
    cursor = connection.cursor()
    subject_search = ""
    if isinstance(subject_name, list):
        subs = ""
        if len(subject_name) > 1:
            for i, s in enumerate(subject_name):
                if i == len(subject_name)-1:
                    subs += '"' + s + '"'
                else:
                    subs += '"' + s + '"' + ','
            subject_search =  'IN ({subject})'.format(subject = subs)
        else:
             subject_search =  'LIKE "%{subject}%"'.format(subject = subject_name[0])

    else:
        subject_search =  'LIKE "%{subject}%"'.format(subject = subject_name)


    cursor.execute('SELECT DISTINCT e.*, COUNT(mL.exerciseList_id) * (AVG(mL.rating) / 5) as popularity FROM (exerciseList e, programmingLanguage pL, user u) '
                    ' LEFT JOIN hasSubject h ON e.id = h.exerciseList_id'
                    ' LEFT JOIN madeList mL ON e.id = mL.exerciseList_id '
                    ' LEFT JOIN subject s ON e.id = h.exerciseList_id AND h.subject_id = s.id'
                    ' WHERE s.name {subject} AND e.name LIKE "%{name}%" AND u.id = e.created_by AND u.first_name LIKE "%{first_name}%" '
                    ' AND u.last_name LIKE "%{last_name}%"'
                    ' AND pL.id = e.prog_lang_id AND pL.name LIKE "{prog_lang}"'
                    ' AND e.difficulty <= {max_diff} AND e.difficulty >= {min_diff}'
                    ' GROUP BY e.name ORDER BY popularity {order_mode};'
                    .format(name = list_name, min_diff = min_list_difficulty, max_diff = max_list_difficulty, first_name = user_first_name, last_name = user_last_name,
                           prog_lang = prog_lang_name, subject = subject_search, order_mode = order_mode))
    fetched = processData(cursor)
    cursor.close()
    return fetched

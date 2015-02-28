from django.db import connection

cursor = connection.cursor()

def dictfetchall():
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def getAll(table):
    cursor.execute('show tables like "{}"'.format(table))
    if(len(dictfetchall()) > 0):
        cursor.execute('SELECT * FROM ' + table)
        return dictfetchall()
    return None

def getUserOnId(id):
    cursor.execute('SELECT * FROM user WHERE user.id = {}'.format(id))
    return processOne()

def getUserOnEmail(email):
    cursor.execute('SELECT * FROM user WHERE user.email = "{}"'.format(email))
    return processOne()

def processData():
    '''
    @brief gets the data from a sql query
    @return returns a dict with the retrieved data
    '''
    info = dictfetchall()
    if not info:
        return None
    else:
        return info

def processOne():
    '''
    @brief gets the data from a sql query
    @return returns a dict with the retrieved data
    '''
    info = dictfetchall()
    if not info:
        return None
    else:
        return info[0]



def createNewUser(first_name, last_name, email, password):
    cursor.execute('INSERT INTO user(is_active, first_name, last_name, password, email) VALUES ({}, "{}", "{}", "{}", "{}");'.format(1, first_name,last_name,password,email))

    cursor.execute('SELECT * FROM user WHERE user.id = {id};'.format(id = id))
    return processData()

def getExerciseListInformation(id):
    '''
    @brief get the information from Exercise lists given an user id
    @param id the id of the user
    @return returns a dict with information
    '''
    cursor.execute('SELECT * FROM exerciseList WHERE id = {id};'.format(id = id))
    return processOne()

def getGroupInformation(id):
    '''
    @brief get the information from Groups given an group id
    @param id the id of the group
    @return returns a dict with information
    '''
    cursor.execute('SELECT * FROM groups WHERE id = {id};'.format(id = id))
    return processOne()

def getExerciseInformation(id):
    '''
    @brief get the information from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor.execute('SELECT e.*, c.code_text, l.name AS language, q.question_text, a.answer_text, a.answer_number, p.name AS programming_language FROM programmingLanguage p, associatedWith aW, correctAnswer cA, answer a, code c, exercise e, language l, question q WHERE e.id = {id} AND e.id = c.exercise_id  AND e.id = q.exercise_id AND q.language_id = l.id AND e.id = cA.exercise_id AND cA.exercise_id = a.id AND e.id = aW.exercise_id AND aW.progLang_id = p.id;'.format(id = id))
    return processOne()

def getExerciseLanguage(id):
    '''
    @brief get the language from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor.execute('SELECT p.name FROM programmingLanguage p, associatedWith a, exercise e WHERE e.id = {id} AND e.id = a.exercise_id AND a.progLang_id = p.id;'.format(id = id))
    return processData()

def getExerciseCode(id):
    '''
    @brief get the code from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor.execute('SELECT c.code_text FROM code c, exercise e WHERE e.id = {id} AND e.id = c.exercise_id;'.format(id = id))
    return processOne()

def getExercQuestionAndLang(id):
    '''
    @brief get the Question and language from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor.execute('SELECT l.name, q.question_text FROM language l, question q, exercise e WHERE e.id = {id} AND e.id = q.exercise_id AND q.language_id = l.id;'.format(id = id))
    return processData()

def getExercCorrectAnswer(id):
    '''
    @brief get the information from Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with information
    '''
    cursor.execute('SELECT a.answer_text, a.answer_number FROM correctAnswer c, answer a, exercise e WHERE e.id = {id} AND e.id = c.exercise_id AND c.exercise_id = a.id ;'.format(id = id))
    return processData()

def getExerciseAnswers(id, languageName):
    '''
    @brief get the answers for a Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with answers
    '''
    cursor.execute('SELECT a.answer_text, a.answer_number  FROM  answer a, exercise e, language l WHERE e.id = {id} AND a.is_answer_for = e.id AND a.language_id = l.id AND l.name = "{l_name}";'.format(id = id, l_name = languageName))
    return processData()

def getExerciseHints(id):
    '''
    @brief get the hints for a Exercise given an exercise id
    @param id the id of the exercise
    @return returns a dict with hints
    '''
    cursor.execute('SELECT h.hint_text, h.hint_number  FROM exercise e, hint h WHERE e.id = h.exercise_id AND e.id = {id};'.format(id = id))
    return processData()

def getFriendsIdForID(id):
    '''
    @brief gets the friends of a user a user id
    @param id the id of the user
    @return returns a dict with friends (hopefully)
    '''
    cursor.execute('SELECT f.friend_id FROM friendsWith f, user u WHERE u.id = f.user_id AND u.id = {id};'.format(id = id))
    return processData()

def getExercisesForList(list_id):
    '''
    @brief gets the exercises in a list given a list id
    @param id the id of the list
    @return returns a dict with exercises
    '''
    cursor.execute('SELECT i.exercise_id FROM exerciseList eL, isPartOf i WHERE eL.id = {id} AND i.exerciseList_id = eL.id;'.format(id = list_id))
    return processData()

def getMadeListForUser(id):
    '''
    @brief gets the exercises list a user finished given a user id
    @param id the id of the user
    @return returns a dict with lists
    '''
    cursor.execute('SELECT * FROM user u, madeList m WHERE  u.id = {id} AND u.id = m.user_id;'.format(id = id))
    return processData()

def getExerciseScoreFor(id, exercise_list):
    '''
    @brief gets the scores of exercises from a user in a certain exercise list
    @param id the id of the user
    @param exercise_list the id of the exercise list
    @return returns a dict with lists
    '''
    cursor.execute('SELECT mE.exercise_id, mE.solved, mE.exercise_score, mE.rating FROM user u, exerciseList eL, isPartOf i, madeEx mE WHERE u.id = {u_id} AND eL.id = {el_id} AND i.exerciseList_id = eL.id AND i.exercise_id =  mE.exercise_id AND mE.user_id = u.id;'.format(u_id = id, el_id = exercise_list))
    return processData()

def getSubjectsForList(list_id):
    '''
    @brief gets the subject of exercise list
    @param list_id the id of the exercise list
    @return returns a dict with lists
    '''
    cursor.execute('SELECT s.name FROM exerciseList e, subject s, hasSubject hS WHERE e.id = hS.exerciseList_id AND hS.subject_id = s.id AND e.id = {id};'.format(id = list_id))
    return processData()

def getPermForUserInGroup(user_id, group_id):
    '''
    @brief gets the permission for a certain user in a certain group
    @param user_id the id of the user
    @param group_id the id of the group
    @return returns a dict with lists
    '''
    cursor.execute('SELECT uIG.user_permissions FROM user u, groups g, userInGroup uIG WHERE u.id = {u_id} AND g.id = {g_id} AND uIG.user_id = u.id AND g.id = uIG.group_id;'.format(u_id = user_id, g_id = group_id))
    return processOne()

def getUsersInGroup(group_id):
    '''
    @brief gets the users in a group
    @param group_id the id of the group
    @return returns a dict with lists
    '''
    cursor.execute('SELECT user_id FROM userInGroup u WHERE u.group_id = {id};'.format(id = group_id))
    return processData()

def getGroupsFromUser(user_id):
    '''
    @brief gets the groups a user is in
    @param user_id the id of the user
    @return returns a dict with lists
    '''
    cursor.execute('SELECT group_id FROM userInGroup u WHERE u.user_id = {id};'.format(id = user_id))
    return processData()

def getIdFromProgrammingLanguage(name):
        '''
        @brief gets the id that corresponds to a given programming language
        @param name the name of the programming_language
        @return returns an integer (the id)
        '''
        cursor.execute('SELECT id FROM programmingLanguage WHERE programmingLanguage.name = {name};'.format(name = name))
        return processOne()

def getMaxIdFromExListForUserID(user_id):
    '''

    '''
    cursor.execute('SELECT max(e.id) AS max FROM exerciseList e WHERE e.created_by = {id};'.format(id = user_id))
    return processOne()


def getNameFromProgLangID(ID):
    cursor.execute('SELECT p.name FROM programmingLanguage p WHERE p.id = {id};'.format(id = ID))
    return processOne()

##INSERTS
def insertIntoTable(tableName, **kwargs):
    columnNames = []
    for key in kwargs.keys():
        columnNames.append('%(' + key + ')s')
    queryColumns = ', '.join(kwargs.keys())
    queryValues = ', '.join(columnNames)
    cursor.execute('INSERT INTO ' + tableName + '('+ queryColumns  +') VALUES ('+ queryValues +');', kwargs)

def insertUser(first_name, last_name, password, email, is_active = 1):
    cursor.execute('INSERT INTO user(is_active,first_name,last_name,password,email) VALUES ({active},"{fname}","{lname}","{passw}","{email}");'.format(active = is_active, fname = first_name, lname = last_name, passw = password, email = email))

def insertFriendsWith(user_id, friend_id):
    cursor.execute('INSERT INTO friendsWith(first_id,second_id) VALUES ({u_id}, {f_id});'.format(u_id = user_id, f_id = friend_id))

def insertGroup(group_name, group_type):
    cursor.execute('INSERT INTO groups(group_name,group_type) VALUES ("{name}", {type});'.format(name = group_name, type = group_type))

def insertUserInGroup(group_id, user_id, user_permissions):
    cursor.execute('INSERT INTO userInGroup(group_id,user_id,user_permissions) VALUES ({g_id}, {u_id}, {u_perm});'.format(g_id = group_id, u_id = user_id, u_perm = user_permissions))

def insertProgrammingLanguage(name):
    cursor.execute('INSERT INTO programmingLanguage(name) VALUES ("{name}");'.format(name = name))

def insertExercise(difficulty, max_score, penalty, exercise_type,created_by, created_on, exercise_number):
    cursor.execute('INSERT INTO exercise(difficulty,max_score,penalty,exercise_type, created_by, created_on, exercise_number) VALUES ({diff},{m},{pen},"{e_type}", {crtd_by}, {crtd_on}, {exerc_nmbr});'.format(diff = difficulty, m = max_score, pen = penalty, e_type = exercise_type, crtd_by = created_by, crtd_on = created_on, exerc_nmbr = exercise_number))
    # Returns last added id (keeps on counting even through deletes?) AKA the one just added
    cursor.execute('SELECT MAX(id) AS highest_id FROM exercise WHERE exercise.created_by = {created_by};'.format(created_by = created_by))
    return processOne()

def insertCode(code_text, exercise_id):
    cursor.execute('INSERT INTO code(code_text, exercise_id) VALUES ("{c_text}", {exerc_id});'.format(c_text = code_text, exerc_id = exercise_id))

def insertAssociatedWith(progLang_id, exercise_id):
    cursor.execute('INSERT INTO associatedWith(progLang_id,exercise_id) VALUES ({pl_id},{e_id});'.format(pl_id = progLang_id, e_id = exercise_id))

def insertLanguage(name):
    cursor.execute('INSERT INTO language(name) VALUES ("{name}");'.format(name = name))

def insertQuestion(question_text, language_id, exercise_id):
    cursor.execute('INSERT INTO question(question_text,language_id,exercise_id) VALUES ("{q_text}",{l_id},{e_id});'.format(q_text = question_text, l_id = language_id, e_id = exercise_id))

def insertAnswer(id, answer_number, answer_text, language_id, is_answer_for):
    cursor.execute('INSERT INTO answer(id, answer_number,answer_text,language_id,is_answer_for) VALUES ({id},{a_numb},"{a_text}",{l_id},{ans_for});'.format(id = id, a_numb = answer_number, a_text = answer_text, l_id = language_id, ans_for = is_answer_for))

def insertHint(hint_text, hint_number, exercise_id):
    cursor.execute('INSERT INTO hint(hint_text,hint_number,exercise_id) VALUES ("{h_text}",{h_numb},{e_id});'.format(h_text = hint_text, h_numb = hint_number, e_id = exercise_id))

def insertExerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id):
    cursor.execute('INSERT INTO exerciseList(name,description,difficulty, created_by, created_on, prog_lang_id) VALUES ("{name}","{desc}",{diff}, {crtd_by}, "{crtd_on}", {prog_lang_id});'.format(name = name, desc = description, diff = difficulty, crtd_by = created_by, crtd_on = created_on, prog_lang_id = prog_lang_id))

def insertSubject(name):
    cursor.execute('INSERT INTO subject(name) VALUES ("{name}");'.format(name = name))

def insertHasSubject(exerciseList_id, subject_id):
    cursor.execute('INSERT INTO hasSubject(exerciseList_id,subject_id) VALUES ({e_id},{s_id});'.format(e_id = exerciseList_id, s_id = subject_id))

def insertIsPartOf(exerciseList_id, exercise_id):
    cursor.execute('INSERT INTO isPartOf(exerciseList_id,exercice_id) VALUES ({el_id},{e_id});'.format(el_id = exerciseList_id, e_id = exercise_id))

def insertCorrectAnswer(exercise_id ,answer_id):
    cursor.execute('INSERT INTO correctAnswer(exercise_id,answer_id) VALUES ({e_id},{a_id});'.format(e_id = exercise_id, a_id = answer_id))

def insertMadeList(exerciseList_id, user_id, rating, score):
    cursor.execute('INSERT INTO madeList(exerciseList_id,user_id,rating,score) VALUES ({el_id},{u_id},{rating},{score});'.format(el_id = exerciseList_id, u_id = user_id, rating = rating, score = score))

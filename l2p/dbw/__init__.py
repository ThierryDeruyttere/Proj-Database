from django.db import connection

cursor = connection.cursor()

def dictfetchall():
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def getAll(table):
    cursor.execute('SELECT * FROM ' + table)
    return dictfetchall()

def getUserOnId(id):
    cursor.execute("SELECT * FROM user WHERE user.id = " + "'%s'" % id)
    return processOne()

def getUserOnEmail(email):
    cursor.execute("SELECT id, first_name, password, email FROM user WHERE user.email = " + "'%s'" % email)
    return processOne()

def processOne():
    info = dictfetchall()
    if not info:
        return None
    else:
        return info[0]

def createNewUser(first_name, last_name, email, password):
    cursor.execute("INSERT INTO user(is_active, first_name, last_name, password, email) VALUES ({}, '{}', '{}', '{}', '{}');".format(1, first_name,last_name,password,email))

    cursor.execute("SELECT * FROM user WHERE user.id = " + "'%s'" % id)
    return processOne()

def getExerciseListInformation(id):
    cursor.execute("SELECT * FROM exerciseList WHERE user.id = " + "'%s'" % id)
    return processOne()

def getExerciseInformation(id):
    cursor.execute("SELECT * FROM exercise WHERE user.id = " + "'%s'" % id)
    return processOne()

def getGroupInformation(id):
    cursor.execute("SELECT * FROM groups WHERE user.id = " + "'%s'" % id)
    return processOne()

def getExerciseLanguage(id):
    cursor.execute("SELECT p.name FROM programmingLanguage p, associatedWith a, exercise e WHERE e.id = {} AND e.id = a.exercise_id AND a.progLang_id = p.id;".format(id))
    return processOne()

def getExerciseCode(id):
    cursor.execute("SELECT c.code_text FROM code c, isCodeFor i, exercise e WHERE e.id = {} AND e.id = i.exercise_id AND i.code_id = c.id;".format(id))
    return processOne()

def getExercQuestionAndLang(id):
    cursor.execute("SELECT l.name, q.question_text  FROM language l, question q, exercise e WHERE e.id = {} AND e.id = q.exercise_id AND q.language_id = l.id;".format(id))
    return processOne()

def getExercCorrectAnswer(id):
    cursor.execute("SELECT a.answer_text, a.answer_number FROM correctAnswer c, answer a, exercise e WHERE e.id = {} AND e.id = c.exercise_id AND c.exercise_id = a.id ;".format(id))
    return processOne()

def getExerciseAnswers(id, languageName):
    cursor.execute("SELECT a.answer_text, a.answer_number  FROM  answer a, exercise e, language l WHERE e.id = 1 AND a.is_answer_for = e.id AND a.language_id = l.id AND l.name = '{}';".format(id, languageName))
    return processOne()

def getExerciseHints(id):
    cursor.execute("SELECT h.hint_text, h.hint_number  FROM exercise e, hint h WHERE e.id = h.exercise_id AND e.id = {};".format(id))
    return processOne()

def getFriendsIdForID(id):
    cursor.execute("select f.friend_id from friendsWith f, user u WHERE u.id = f.user_id AND u.id = {};".format(id))
    return processOne()

def getExercisesForList(list_id):
    cursor.execute("select i.exercise_id FROM exerciseList eL, isPartOf i WHERE eL.id = {} AND i.exerciseList_id = eL.id;".format(list_id))
    return processOne()

def getMadeListForUser(id):
    cursor.execute("select * from  user u, madeList m WHERE  u.id = {} AND u.id = m.user_id;".format(id))
    return processOne()

def getExerciseScoreFor(id, exercise_list):
    cursor.execute("select mE.exercise_id, mE.solved, mE.exercise_score, mE.rating from  user u, exerciseList eL, isPartOf i, madeEx mE WHERE u.id = 1 AND eL.id = 1 AND i.exerciseList_id = eL.id AND i.exercise_id =  mE.exercise_id AND mE.user_id = u.id;".format(id, exercise_list))
    return processOne()

def getSubjectsForList(list_id):
    cursor.execute("select s.name from exerciseList e, subject s, hasSubject hS WHERE e.id = hS.exerciseList_id AND hS.subject_id = s.id AND e.id = {};".format(list_id))
    return processOne()

def getPermForUserInGroup(user_id, group_id):
    cursor.execute("select uIG.user_permissions from user u, groups g, userInGroup uIG WHERE u.id = {} AND g.id = {} AND uIG.user_id = u.id AND g.id = uIG.group_id;".format(user_id, group_id))
    return processOne()

##INSERTS
def insertIntoTable(tableName, **kwargs):
    columnNames = []
    for key in kwargs.keys():
        columnNames.append('%(' + key + ')s')
    queryColumns = ', '.join(kwargs.keys())
    queryValues = ', '.join(columnNames)
    cursor.execute("INSERT INTO " + tableName + "("+ queryColumns  +") VALUES ("+ queryValues +");", kwargs)

def insertUser(first_name, last_name, password, email, is_active = 1):
    cursor.execute("INSERT INTO user(is_active, first_name, last_name, password, email) VALUES ({}, '{}', '{}', '{}', '{}');".format(is_active, first_name,last_name,password,email))

def insertFriendsWith(user_id, friend_id):
    cursor.execute("INSERT INTO friendsWith(first_id, second_id) VALUES ({}, {});".format(user_id, friend_id))

def insertGroup(group_name, group_type):
    cursor.execute("INSERT INTO groups(group_name, group_type) VALUES ('{}', {});".format(group_name, group_type))

def insertUserInGroup(group_id, user_id, user_permissions):
    cursor.execute("INSERT INTO userInGroup(group_id, user_id, user_permissions) VALUES ({}, {}, {});".format(group_id, user_id, user_permissions))

def insertProgrammingLanguage(name):
    cursor.execute("INSERT INTO programmingLanguage(name) VALUES ('{}');".format(name))

def insertExercise(difficulty, max_score, penalty, exercise_type):
    cursor.execute("INSERT INTO exercise(difficulty, max_score, penalty, exercise_type) VALUES ({},{},{},'{}');".format(difficulty, max_score, penalty, exercise_type))

def insertCode(code_text):
    cursor.execute("INSERT INTO code(code_text) VALUES ('{}');".format(code_text))

def insertAssociatedWith(progLang_id, exercise_id):
    cursor.execute("INSERT INTO associatedWith(progLang_id, exercise_id) VALUES ({},{});".format(progLang_id, exercise_id))

def insertIsCodeFor(code_id, exercise_id):
    cursor.execute("INSERT INTO isCodeFor(code_id, exercise_id) VALUES ({},{});".format(code_id, exercise_id))

def insertLanguage(name):
    cursor.execute("INSERT INTO language(name) VALUES ('{}');".format(name))

def insertQuestion(question_text, language_id, exercise_id):
    cursor.execute("INSERT INTO question(question_text, language_id, exercise_id) VALUES ('{}',{},{});".format(question_text, language_id, exercise_id))

def insertAnswer(id, answer_number, answer_text, language_id, is_answer_for):
    cursor.execute("INSERT INTO answer(id, answer_number, answer_text, language_id, is_answer_for) VALUES ({},{},'{}', {},{});".format(id,answer_number, answer_text, language_id, is_answer_for))

def insertHint(hint_text, hint_number, exercise_id):
    cursor.execute("INSERT INTO hint(hint_text, hint_number, exercise_id) VALUES ('{}', {}, {});".format(hint_text, hint_number, exercise_id))

def insertExerciseList(name, description ,difficulty):
    cursor.execute("INSERT INTO exerciseList(name, description ,difficulty) VALUES ('{}', '{}', {});".format(name, description ,difficulty))

def insertSubject(name):
    cursor.execute("INSERT INTO subject(name) VALUES ('{}');".format(name))

def insertHasSubject(exerciseList_id, subject_id):
    cursor.execute("INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES ({},{});".format(exerciseList_id, subject_id))

def insertIsPartOf(exerciseList_id, exercise_id):
    cursor.execute("INSERT INTO isPartOf(exerciseList_id, exercice_id) VALUES ({},{});".format(exerciseList_id, exercise_id))

def insertCorrectAnswer(exercise_id ,answer_id):
    cursor.execute("INSERT INTO correctAnswer(exercise_id ,answer_id) VALUES ({},{});".format(exercise_id ,answer_id))

def insertMadeList(exerciseList_id, user_id, rating, score):
    cursor.execute("INSERT INTO madeList(exerciseList_id, user_id, rating, score) VALUES ({},{},{},{});".format(exerciseList_id, user_id, rating, score))

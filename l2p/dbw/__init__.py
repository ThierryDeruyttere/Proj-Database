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

def getUser(email):
	cursor.execute("SELECT id, first_name, password, email FROM user WHERE user.email = " + "'%s'" % email)
	return dictfetchall()

def getUserInformation(id):
	cursor.execute("SELECT * FROM user WHERE user.id = " + "'%s'" % id)
	return dictfetchall()

def createNewUser(first_name, last_name, email, password):
    cursor.execute("INSERT INTO user(is_active, first_name, last_name, password, email) VALUES ({}, '{}', '{}', '{}', '{}');".format(1, first_name,last_name,password,email))

def insertIntoTable(tableName, **kwargs):
    columnNames = []
    for key in kwargs.keys():
        columnNames.append('%(' + key + ')s')
    queryColumns = ', '.join(kwargs.keys())
    queryValues = ', '.join(columnNames)
    cursor.execute("INSERT INTO " + tableName + "("+ queryColumns  +") VALUES ("+ queryValues +");", kwargs)

def insertUser(first_name, last_name, password, email, is_active = 1):
    cursor.execute("INSERT INTO user(is_active, first_name, last_name, password, email) VALUES ({}, '{}', '{}', '{}', '{}');".format(is_active, first_name,last_name,password,email))

def insertFriendsWith(first_id, second_id):
    cursor.execute("INSERT INTO friendsWith(first_id, second_id) VALUES ({}, {});".format(first_id, second_id))

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

def insertAnswer(answer_number, answer_text, language_id, is_answer_for):
    cursor.execute("INSERT INTO answer(answer_number, answer_text, language_id, is_answer_for) VALUES ({},'{}', {},{});".format(answer_number, answer_text, language_id, is_answer_for))

def insertHint(hint_text, hint_number, exercise_id):
    cursor.execute("INSERT INTO hint(hint_text, hint_number, exercise_id) VALUES ('{}', {}, {});".format(hint_text, hint_number, exercise_id))

def insertExerciseList(name, description ,difficulty):
    cursor.execute("INSERT INTO exerciseList(name, description ,difficulty) VALUES ({}', '{}', {});".format(name, description ,difficulty))

def insertSubject(name):
    cursor.execute("INSERT INTO subject(name) VALUES ('{}');".format(name))

def insertHasSubject(exerciseList_id, subject_id):
    cursor.execute("INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES ({},{});".format(exerciseList_id, subject_id))

def insertIsPartOf(exerciseList_id, exercice_id):
    cursor.execute("INSERT INTO isPartOf(exerciseList_id, exercice_id) VALUES ({},{});".format(exerciseList_id, exercice_id))

def insertCorrectAnswer(exercise_id ,answer_id):
    cursor.execute("INSERT INTO correctAnswer(exercise_id ,answer_id) VALUES ({},{});".format(exercise_id ,answer_id))
>>>>>>> 457e0c6bce1ad24ec7f6c1f68c70d8f62c5b13de

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
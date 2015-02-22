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

def getUser(username):
	cursor.execute("SELECT id, first_name, password FROM user WHERE user.first_name = " + "'%s'" % username)
	return dictfetchall()

def getUserInformation(id):
	cursor.execute("SELECT * FROM user WHERE user.id = " + "'%s'" % id)
	return dictfetchall()
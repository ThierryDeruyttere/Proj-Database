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

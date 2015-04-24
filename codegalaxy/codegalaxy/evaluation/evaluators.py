"""
File for all custom Evaluator classes.

Usage:
- One class per language.
- Call super in init with (lang_name, file_extension, code).
- Override 'evaluate' method.
- Optional: Override getErrorMsg to do error highlighting

Functions to use:
- command(command, args=[])
- codeFile[Name]: Handle to code file or filename
- outputFile[Name]: Handle to output file or filename
- hasError: bool to check if the last command had an error
"""

import os
import subprocess

from django.db import connections

from codegalaxy.evaluation.baseEvaluator import *

class EvaluatorPython(Evaluator):

    """ Code Evaluator for Python """

    def __init__(self, code):
        super(EvaluatorPython, self).__init__('python', 'py', code)

    def evaluate(self):
        self.command('python3', ['-I', '-c', self.code])

class EvaluatorCpp(Evaluator):

    """ Code Evaluator for C++ """

    def __init__(self, code):
        super(EvaluatorCpp, self).__init__('cpp', 'cpp', code)

    def evaluate(self):
        # Compile with the file 'g++'
        self.command('g++', ['-Wall', '-o', self.outputFileName(), self.codeFileName()])
        # If the compile command had an error, output it
        if self.error:
            return
        # Run the outputfile
        self.command(self.outputFileName())

class EvaluatorSql(Evaluator):

    def __init__(self, code, user=0):
        self.db_name = str(user)
        super(EvaluatorSql, self).__init__('sql', 'sql', code)

    def evaluate(self):
        cursor = connections['sandbox'].cursor()
        cursor.execute(self.code)

    def getOutput(self, is_editor):
        cursor = connections['sandbox'].cursor()
        cursor.execute('SHOW TABLES;')
        tables = cursor.fetchall()
        output = '<div class="row">'
        for table in tables:
            print(table[0])
            cursor.execute('SELECT * FROM ' + str(table[0]) + ';')
            output += '<div class="large-3 columns end">'
            output += table[0]
            output += '<table><thead>'
            for col in cursor.description:
                output += '<td>' + col[0] + '</td>'
            output += '</thead>'
            for row in list(cursor.fetchall()):
                output += '<tr>'
                for col in list(row):
                    output += '<td>' + str(col) + '</td>'
                output += '</tr>'
            output += '</table></div>'

        output += '</div>'
        return output

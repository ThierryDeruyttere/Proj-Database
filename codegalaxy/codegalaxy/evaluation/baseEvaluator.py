import os
import subprocess

class Response:
    def __init__(self, output, error):
        self.output = output
        self.error = error

    def __str__(self):
        return str({'output': self.output, 'error': self.error})

class Evaluator:
    """Base class for all code evaluators"""

    def __init__(self, type, extension, code):
        self.type = type
        self.code = code
        self.extension = extension

        self.codeToFile()

    def evaluate(self):
        raise 'Evaluator.evaluate not implemented'

    def codeFile(self):
        return open(self.codeFileName(), 'w')

    def codeFileName(self):
        return os.path.join('tmp', 'code', self.type + '.' + self.extension)

    def outputFile(self):
        return open(self.outputFileName(), 'r')

    def outputFileName(self):
        return os.path.join('tmp', 'output', self.type)

    def codeToFile(self):
        self.codeFile().write(self.code)

    def command(self, command, args=[]):
        args.insert(0, command)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        response = p.communicate()
        return Response(response[0], response[1])

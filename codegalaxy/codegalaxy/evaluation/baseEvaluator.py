import os
import subprocess

# TODO: Commenting

class Evaluator:

    """Base class for all code evaluators"""

    def __init__(self, type, extension, code):
        self.type = type
        self.code = code
        self.extension = extension

        self.output = ''
        self.error = ''

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
        with open(self.codeFileName(), 'w') as f:
            f.write(self.code)

    def command(self, command, args=[], sh=False):
        if not sh:
            cmd = args
            args.insert(0, command)
        else:
            cmd = command + ' ' + ' '.join(args)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=sh)
        response = p.communicate()
        self.output, self.error = response

    def hasError(self):
        return not self.error == ''

    def getErrorMsg(self, is_editor):
        if is_editor:
            return '<pre>' + self.error + '<pre>'
        else:
            return self.error

    def getOutput(self, is_editor):
        if is_editor:
            return '<pre>' + self.output + '<pre>'
        else:
            return self.output

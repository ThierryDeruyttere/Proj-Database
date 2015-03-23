import os
import subprocess

from codegalaxy.evaluation.baseEvaluator import *

class EvaluatorPython(Evaluator):
    """docstring for PythonEval"""
    def __init__(self, code):
        super(EvaluatorPython, self).__init__('python', 'py', code)

    def evaluate(self):
        return 'success!'

class EvaluatorCpp(Evaluator):
    """docstring for PythonEval"""
    def __init__(self, code):
        super(EvaluatorCpp, self).__init__('cpp', 'cpp', code)

    def evaluate(self):
        # Compile with the file 'g++'
        self.command('g++', ['-Wall', '-o', self.outputFileName(), self.codeFileName()])
        # If the compile command had an error, output it
        if self.error:
            return
        # Run the outputfile and put it in the output
        self.command(self.outputFileName())

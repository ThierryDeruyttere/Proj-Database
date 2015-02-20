class Exercise:
    '''An Exercise-object holds all the information of a single exercise that
    is needed, meaning the additional data from other tables aswell'''
    def __init__(self):
        self.id
        # (Integer ranging from 1-5)
        self.difficulty
        # you start at the max_score, and with each wrong guess
        # the penalty gets substracted from it
        self.max_score
        self.penalty
        # states whether an exercise is multiple choice or a coding one
        self.exercise_type
        # Programming language the question is about (string)
        self.programming_language
        # the given code to add upon (string)
        self.code
        # Question asked to the user (string)
        self.question
        # Language the question is in (string)
        self.language
        # List of possible answerIDs (only one in a coding exercise = the output)
        self.answers
        # ID of the correct answer
        self.correct_answer
        # List of strings depicting hints
        self.hints

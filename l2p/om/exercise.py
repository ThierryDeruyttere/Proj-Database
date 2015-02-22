class Exercise:
    '''An Exercise-object holds all the information of a single exercise that
    is needed, meaning the additional data from other tables aswell'''
    def __init__(self,id,difficulty,max_score,penalty,exercise_type,programming_language,code,question,language,correct_answer):
        self.id = id
        # (Integer ranging from 1-5)
        self.difficulty = difficulty
        # you start at the max_score, and with each wrong guess
        # the penalty gets substracted from it
        self.max_score = max_score
        self.penalty = penalty
        # states whether an exercise is multiple choice or a coding one
        self.exercise_type = exercise_type
        # Programming language the question is about (string)
        self.programming_language = programming_language
        # the given code to add upon (string)
        self.code = code
        # Question asked to the user (string)
        self.question = question
        # Language the question is in (string)
        self.language = language
        # ID of the correct answer
        self.correct_answer = correct_answer

        # List of possible answerIDs (only one in a coding exercise = the output)
        def allAnswers():
            pass

        # List of strings depicting hints
        def allHints():
            pass

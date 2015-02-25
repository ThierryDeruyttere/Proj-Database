def strbin(s):
    return ''.join(format(ord(i),'0>8b') for i in s)

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
        self.code = code.decode('ascii')
        # Question asked to the user (string)
        self.question = question.decode('ascii')
        # Language the question is in (string)
        self.language = language
        # ID of the correct answer
        self.correct_answer = correct_answer.decode('ascii')

    def __str__(self):
        return str(self.difficulty)+' '+str(self.max_score)+' '+str(self.penalty)+' '+self.exercise_type+' '+self.programming_language+' '+self.code+' '+self.question+' '+self.language+' '+self.correct_answer

    # List of possible answerIDs (only one in a coding exercise = the output)
    def allAnswers(self):
        answer_info = dbw.getExerciseAnswers(self.id,self.language)
        if answer_info:
            # first we add the data to a list of tuples
            answer_unordered_list = [(x['answer_text'],x['answer_number']) for x in answer_info]
            # We sort on the second element of every tuple
            sorted_answers = sorted(answer_unordered_list, key=lambda tup: tup[1])
            # We don't need the number anymore
            short_list = [answer[0] for answer in sorted_answers]
            return short_list
        else:
            return None

    # List of strings depicting hints
    def allHints(self):
        hint_info = dbw.getExerciseHints(self.id)
        if hint_info:
            # first we add the data to a list of tuples
            hint_unordered_list = [(x['hint_text'],x['hint_number']) for x in hint_info]
            # We sort on the second element of every tuple
            sorted_hints = sorted(hint_unordered_list, key=lambda tup: tup[1])
            # We don't need the number anymore
            short_list = [hint[0] for hint in sorted_hints]
            return short_list
        else:
            return None

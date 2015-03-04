import dbw

class Exercise:
    '''An Exercise-object holds all the information of a single exercise that
    is needed, meaning the additional data from other tables aswell'''
    def __init__(self,id,difficulty,max_score,penalty,exercise_type,programming_language
    ,code,question,language_code,correct_answer,language_name):
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
        self.language_name = language_name
        # ID of the correct answer
        self.correct_answer = correct_answer.decode('ascii')
        # Django code for the name
        self.language_code = language_code

    def __str__(self):
        return str(self.difficulty)+' '+str(self.max_score)+' '+str(self.penalty)+' '+str(self.exercise_type)+' '+str(self.programming_language)+' '+self.code+' '+self.question+' '+self.language_name+' '+str(self.correct_answer)+' '+str(self.language_code)

    # List of possible answerIDs (only one in a coding exercise = the output)
    def allAnswers(self):
        answer_info = dbw.getExerciseAnswers(self.id,self.language_name)
        if answer_info:
            # first we add the data to a list of tuples
            answer_unordered_list = [(x['answer_text'],x['answer_number']) for x in answer_info]
            # We sort on the second element of every tuple
            sorted_answers = sorted(answer_unordered_list, key=lambda tup: tup[1])
            # We don't need the number anymore
            short_list = [answer[0].decode('ascii') for answer in sorted_answers]
            return short_list
        else:
            return None

    # List of strings depicting hints
    def allHints(self):
        hint_info = dbw.getExerciseHints(self.id,self.language_name)
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

    #inserts a list of answer_texts (also deletes the previous ones)
    def updateAnswers(self,answers):
        dbw.deleteAnswers(self.id)
        language_id = dbw.getIdFromLanguage(self.language_code)['id']
        print(language_id)
        for i in range(len(answers)):
            dbw.insertAnswer(i, answers[i], language_id, self.id)

    #inserts a list of answer_texts (also deletes the previous ones)
    def updateHints(self,hints):
        dbw.deleteHints(self.id)
        language_id = dbw.getIdFromLanguage(self.language_code)['id']
        print(language_id)
        for i in range(len(hints)):
            dbw.insertHint(hints[i], i, self.id, language_id)

    def update(self,correct_answer,answers,hints):
        self.correct_answer = correct_answer
        self.updateAnswers(answers)
        self.updateHints(hints)

    def save(self):
        dbw.updateExercise(id,self.difficulty, self.max_score, self.penalty, self.exercise_type, self.created_by, self.created_on, self.exercise_number, self.correct_answer, self.exerciseList_id)

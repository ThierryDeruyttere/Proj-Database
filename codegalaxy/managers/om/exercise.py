import dbw

def decodeString(fromVar):
    decoded = ""
    try:
        decoded = fromVar.decode('ascii')
    except AttributeError:
        decoded = fromVar
    return decoded


class Exercise:

    '''An Exercise-object holds all the information of a single exercise that
    is needed, meaning the additional data from other tables aswell'''

    def __init__(self, id, difficulty, max_score, penalty, exercise_type, programming_language, code, question, language_code, correct_answer, language_name, title):
        '''
        @brief init for a exercise
        @param id id of the exercise
        @param difficulty difficulty of the exercise
        @param max_score max score for the exercise
        @param penalty a penalty for each wrong answer
        @param exercise_type the type of the exercise
        @param programming_language the programming language for which the exercise is made
        @param code the code for the exercise, if any!
        @param question the question of the exercise
        @param language_code the language code for example En-us
        @param correct_answer the number of the correct answer for this exercise
        @param language_name the name of the language (English, etc..)
        @param title the title of the exercise
        '''
        self.id = int(id)
        # (Integer ranging from 1-5)
        self.difficulty = int(difficulty)
        # you start at the max_score, and with each wrong guess
        # the penalty gets substracted from it
        self.max_score = int(max_score)
        self.penalty = int(penalty)
        # states whether an exercise is multiple choice or a coding one
        self.exercise_type = exercise_type
        # Programming language the question is about (string)
        self.programming_language = programming_language
        # the given code to add upon (string)
        self.code = decodeString(code)
        # Question asked to the user (string)
        self.question = decodeString(question)
        # Language the question is in (string)
        self.language_name = language_name
        # ID of the correct answer
        self.correct_answer = int(correct_answer)
        # Django code for the name
        self.language_code = language_code
        # Exercise title
        self.title = title
        # Exercise is solved
        # Only for giving info to html templates
        self.solved = False

    def __str__(self):
        '''
        @brief string representation of exercise
        '''
        return str(self.difficulty) + ' ' + str(self.max_score) + ' ' + str(self.penalty) + ' ' + str(self.exercise_type) + ' ' + str(self.programming_language) + ' ' + self.code + ' ' + self.question + ' ' + self.language_name + ' ' + str(self.correct_answer) + ' ' + str(self.language_code)

    # List of possible answerIDs (only one in a coding exercise = the output)
    def allAnswers(self):
        '''
        @brief get all the answers for an exercise
        @return returns all the answers for an exercise if there are some else return None
        '''
        answer_info = dbw.getExerciseAnswers(self.id, self.language_name)
        if answer_info:
            # first we add the data to a list of tuples
            answer_unordered_list = [(x['answer_text'], x['answer_number']) for x in answer_info]
            # We sort on the second element of every tuple
            sorted_answers = sorted(answer_unordered_list, key=lambda tup: tup[1])
            # We don't need the number anymore
            short_list = [answer[0].decode('ascii') for answer in sorted_answers]
            return short_list
        else:
            return None

    # List of strings depicting hints
    def allHints(self):
        '''
        @brief get all the hints of an exercise
        @return return all the hints for an exercise if there are some, else return None
        '''
        hint_info = dbw.getExerciseHints(self.id, self.language_name)
        if hint_info:
            # first we add the data to a list of tuples
            hint_unordered_list = [(x['hint_text'], x['hint_number']) for x in hint_info]
            # We sort on the second element of every tuple
            sorted_hints = sorted(hint_unordered_list, key=lambda tup: tup[1])
            # We don't need the number anymore
            short_list = [hint[0] for hint in sorted_hints]
            return short_list
        else:
            return None

    # inserts a list of answer_texts (also deletes the previous ones)
    def updateAnswers(self, answers):
        '''
        @brief update the answers of an exercise
        @param answers the answers to update
        '''
        dbw.deleteAnswers(self.id)
        language_id = dbw.getIdFromLanguage(self.language_code)['id']
        for i in range(1, len(answers) + 1):
            dbw.insertAnswer(i, answers[i - 1], language_id, self.id)

    # inserts a list of answer_texts (also deletes the previous ones)
    def updateHints(self, hints):
        '''
        @brief update the hints of an exercise
        @param hints the hints to update
        '''
        dbw.deleteHints(self.id)
        language_id = dbw.getIdFromLanguage(self.language_code)['id']
        for i in range(1, len(hints) + 1):
            dbw.insertHint(hints[i - 1], i, self.id, language_id)

    def update(self, correct_answer, answers, hints):
        '''
        @brief update an exercise with a correct answer, answers and hints
        @param correct_answer the correct answer to update
        @param answers the answers to update
        @param hints the hints to update
        '''
        self.correct_answer = correct_answer
        self.updateAnswers(answers)
        self.updateHints(hints)

    def save(self):
        '''
        @brief saves the exercise in the database
        '''
        dbw.updateExercise(self.id, self.difficulty, self.max_score, self.penalty, self.exercise_type, self.created_by, self.created_on, self.exercise_number, self.correct_answer, self.exerciseList_id)

class Question:

    def __init__(self, question_text, language_id):
        '''
        @brief init of question
        @param question_text the text of the question
        @param language_id the id of the language
        '''
        self.question_text = question_text
        self.language_id = language_id

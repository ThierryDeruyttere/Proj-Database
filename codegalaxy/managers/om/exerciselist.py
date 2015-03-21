import dbw
import managers.om.exercise
import managers.om.objectmanager

class ExerciseList:

    def __init__(self, id, name, difficulty, description, created_by, created_on, programming_lang):
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.description = description
        self.created_by = created_by
        self.created_on = created_on
        self.programming_language = programming_lang
        self.programming_language_string = dbw.getNameFromProgLangID(programming_lang)['name']

    def __str__(self):
        return self.name + ' ' + str(self.difficulty) + ' ' + self.description + ' ' + str(self.created_by) + ' ' + str(self.created_on)

    def creatorName(self):
        object_manager = managers.om.objectmanager.ObjectManager()
        creator = object_manager.createUser(id = self.created_by)
        return creator.name()

    # List of subjects
    def allSubjects(self):
        subjects_info = dbw.getSubjectsForList(self.id)
        if subjects_info:
            # We'll put the info in a regular list
            subjects_list = [x['name'] for x in subjects_info]
            return subjects_list
        else:
            return None

    def allSubjectIDs(self):
        subjects_info = dbw.getSubjectIDsForList(self.id)
        if subjects_info:
            # We'll put the info in a regular list
            subjects_list = [x['id'] for x in subjects_info]
            return subjects_list
        else:
            return None

    def amountOfUsersWhoMadeThisList(self):
        return dbw.getAmountOfUsersWhoMadeList(self.id)['amount']

    def averageOfUsersForThisList(self):
        return dbw.getAvgScoreOfUsersWhoMadeList(self.id)['average']

    def averageRatingOfUsersForThisList(self):
        return dbw.averageRatingOfUsersWhoMadeList(self.id)['average']

    # List of exercises
    def allExercises(self, language_code):
        # Getting all original exercise_ids
        exercises_infos = dbw.getExercisesForList(self.id)
        # Getting all references
        exercise_references_infos = dbw.getExerciseReferencesForList(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        exercises = []
        if exercises_infos:
            # We'll put the info in a regular list
            exercises = []
            for exercise_id in exercises_infos:
                exercises.append(object_manager.createExercise(exercise_id['id'], language_code))
            if exercise_references_infos:
                for exercise_id in exercise_references_infos:
                    referenced = object_manager.createExercise(exercise_id['id'], language_code)
                    referenced.exercise_number = exercise_id['new_list_exercise_number']
                    exercises.append(referenced)
            return exercises
        else:
            return []

    def getExercise(self, id, language_code):
        for ex in allExercises(language_code):
            if ex.id == id:
                return ex
            else:
                return None

    def hasX(self, id, X_type):
        if X_type == 'Subject':
            return self.hasSubject(id)
        elif X_type == 'Programming Language':
            return self.programming_language == id

    def hasSubject(self, subject_id):
        subjects_info = dbw.getSubjectIDsForList(self.id)
        if subjects_info:
            # We'll put the info in a regular list
            subjects_list = [x['id'] for x in subjects_info]
            return subject_id in subjects_list

    def save(self):
        dbw.updateExerciseList(self.id, self.name, self.description, self.difficulty, self.programming_language)

    def update(self, updated_name, updated_description, updated_difficulty, updated_prog_lang):
        # list_id,name, description ,difficulty, prog_lang_id)
        prog_lang_id = int(dbw.getIdFromProgrammingLanguage(updated_prog_lang)["id"])
        dbw.updateExerciseList(self.id, updated_name, updated_description, updated_difficulty, prog_lang_id)

    def addSubject(self, subject_name):
        dbw.insertSubject(subject_name)
        subject_id = int(dbw.getSubjectID(subject_name)["id"])

        dbw.insertHasSubject(self.id, subject_id)

    def deleteSubject(self, subject_name):
        subject_id = int(dbw.getSubjectID(subject_name)["id"])
        dbw.deleteSubjectFromHasSubject(self.id, subject_id)

    def getAllExercForUserForList(self, user_id):
        return dbw.getAllExercForUserForList(user_id,self.id)


    def insertExercise(self, difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, question, answers, correct_answer, hints, language_code, title, code=""):
        # Info for exercises table + id of the exercise
        exercise_id = dbw.insertExercise(difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, self.id, title)['highest_id']
        # AssociatedWith relation
        l_id = dbw.getIdFromLanguage(language_code)['id']
        # Code (default "")
        if(code != ""):
            dbw.insertCode(code, exercise_id)
        # question = QuestionContainer object
        dbw.insertQuestion(question.question_text, question.language_id, exercise_id)

        import managers.om.objectmanager
        object_manager = managers.om.objectmanager.ObjectManager()

        for i, answer in enumerate(answers):
            dbw.insertAnswer(i + 1, answer, 1, exercise_id)

        for i, hint in enumerate(hints):
            dbw.insertHint(hint, i + 1, exercise_id, l_id)

        exercise = object_manager.createExercise(exercise_id, language_code)

        exercise.update(correct_answer, answers, hints)

    def insertExerciseByReference(self, original_exercise_id, new_list_exercise_number):
        dbw.insertExerciseByReference(original_exercise_id, self.id, new_list_exercise_number)

    def unreferenceExercise(self, exercise_number):
        # to 'unreference' something, we have to add it to the DB
        # NOTE: all the answers and questions and stuff will also have to be added!
        object_manager = managers.om.objectmanager.ObjectManager()
        # first, we'll have to look up what the original exercise was
        original_ex_id = int(dbw.getOriginalExercise(self.id, exercise_number)['original_id'])
        new_id = dbw.copyExercise(original_ex_id, exercise_number)
        #now we need to delete the reference from the DB
        dbw.deleteReference(self.id, exercise_number)
        return new_id

    def getLastExercise(self):
        if dbw.getLastExerciseFromList(self.id)["last_exercise_number"] == None:
            return 0
        else:
            return dbw.getLastExerciseFromList(self.id)["last_exercise_number"]

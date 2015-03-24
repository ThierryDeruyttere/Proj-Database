import dbw
import managers.om.exercise
import managers.om.objectmanager

class ExerciseList:

    def __init__(self, id, name, difficulty, description, created_by, created_on, programming_lang, default_language_code='en'):
        self.id = int(id)
        self.name = name
        self.difficulty = int(difficulty)
        self.description = description
        self.created_by = created_by
        self.created_on = created_on
        self.programming_language = programming_lang
        self.programming_language_string = dbw.getNameFromProgLangID(programming_lang)['name']
        self.default_language_code = default_language_code

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

    def amountOfExercises(self):
        return getAmountOfExercisesForList(self.id)['amount']

    # List of exercises
    def allExercises(self, language_code):
        # we'll need to check if any numbers are missing, so we get the amount of em
        #TODO: wtf doe defaultlang?
        #amount_of_exercises = self.amountOfExercises()
        # Getting all original exercise_ids
        exercises_infos = dbw.getExercisesForList(self.id)
        # Getting all references
        exercise_references_infos = dbw.getExerciseReferencesForList(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        exercises = []
        # We'll put the info in a regular list
        for exercise_id in exercises_infos:
            exercises.append(object_manager.createExercise(exercise_id['id'], language_code))
        for exercise_id in exercise_references_infos:
            referenced = object_manager.createExercise(exercise_id['id'], language_code)
            referenced.exercise_number = exercise_id['new_list_exercise_number']
            exercises.append(referenced)
        # now we sort the exercises on exercise_number
        exercises = sorted(exercises, key=lambda ex: ex.exercise_number)
        return exercises


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
        if code != "":
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

    def getLastExercise(self):
        last = dbw.getLastExerciseFromList(self.id)["last_exercise_number"]
        if last is None:
            return 0
        else:
            return last

    def insertExerciseByReference(self, original_exercise_id):
        new_list_exercise_number = int(self.getLastExercise()) + 1
        dbw.insertExerciseByReference(original_exercise_id, self.id, new_list_exercise_number)
        return new_list_exercise_number

    def unreferenceExercise(self, exercise_number):
        # to 'unreference' something, we have to add it to the DB
        # NOTE: all the answers and questions and stuff will also have to be added!
        object_manager = managers.om.objectmanager.ObjectManager()
        # first, we'll have to look up what the original exercise was
        original_ex_id = int(dbw.getOriginalExercise(self.id, exercise_number)['id'])
        new_id = dbw.copyExercise(original_ex_id, exercise_number, self.id)
        #now we need to delete the reference from the DB
        dbw.deleteReference(self.id, exercise_number)
        return new_id

    def copyExercise(self, original_exercise_id):
        number = self.insertExerciseByReference(original_exercise_id)
        self.unreferenceExercise(number)

    def maxScore(self):
        return dbw.getMaxSumForExForList(self.id) + dbw.getMaxSumForRefForList(self.id)

    # scrambled_exercises is a list of Exercise objects
    def reorderExercises(self, scrambled_exercise_ids, language_code):
        # First we need to convert the list of integers to actual objects
        normal_order = self.allExercises(language_code)
        scrambled_exercises = []
        for ex_number in scrambled_exercise_ids:
            for ex in normal_order:
                if ex.exercise_number == ex_number:
                    scrambled_exercises.append(ex)
                    break
        # First we'll check which exercises were deleted
        # The amount of exercises we had at first
        last_exercise = self.getLastExercise()
        # The missing indices (exercises)
        missing = []
        for i in range(1,last_exercise+1):
            if i not in scrambled_exercise_ids:
                self.deleteExercise(i)

        transaction = ''
        for i in range(len(scrambled_exercises)):
            # we simply change the number to the new indice of the list
            print(str(scrambled_exercises[i].exercise_number) + 'to' + str(i+1))
            scrambled_exercises[i].exercise_number = (i+1)
            transaction += scrambled_exercises[i].saveExerciseNumber()
        dbw.UpdateExerciseAndReferenceNumbers(transaction)

    def deleteExercise(self, exercise_number):
        if dbw.isReference(self.id, exercise_number):
            # Ref -> just delete from DB
            dbw.deleteReference(self.id, exercise_number)
        else:

            object_manager = managers.om.objectmanager.ObjectManager()
            # Not ref -> delete it (all info about it) and dereference all references to it
            # First we need to get all the references to this exercise
            exercise = object_manager.createExercise(dbw.getExerciseInList(self.id, exercise_number)['id'])
            # list of discts with exercise_number and reference
            all_references = object_manager.getAllReferencesTo(exercise.id)
            for reference in all_references:
                exercise_list = object_manager.createExerciseList(reference['list_id'])
                exercise_list.unreferenceExercise(reference['exercise_number'])
            # Now we'll delete the old exercise
            dbw.deleteExercise(exercise.id)

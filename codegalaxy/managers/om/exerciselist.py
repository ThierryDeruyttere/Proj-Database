import dbw
import managers.om.exercise
import managers.om.objectmanager

# Object representation of an exerciselist
class ExerciseList:

    def __init__(self, id, name, difficulty, description, created_by, created_on, programming_lang, default_language_code='en'):
        self.id = int(id)
        self.name = name
        self.difficulty = int(difficulty)
        self.description = description
        self.created_by = created_by
        self.created_on = created_on
        self.programming_language = managers.om.objectmanager.Language(int(programming_lang), dbw.getNameFromProgLangID(programming_lang)['name'])
        self.default_language_code = default_language_code

    def __str__(self):
        return self.name + ' ' + str(self.difficulty) + ' ' + self.description + ' ' + str(self.created_by) + ' ' + str(self.created_on)

    # Returns a User-object of the creator of this list
    def creator(self):
        object_manager = managers.om.objectmanager.ObjectManager()
        creator = object_manager.createUser(id=self.created_by)
        return creator

    # List of names subjects that this list has
    def allSubjects(self):
        subjects_info = dbw.getSubjectsForList(self.id)
        if subjects_info:
            # We'll put the info in a regular list
            subjects_list = [x['name'] for x in subjects_info]
            return subjects_list
        else:
            return None

    # List of ids subjects that this list has
    def allSubjectIDs(self):
        subjects_info = dbw.getSubjectIDsForList(self.id)
        if subjects_info:
            # We'll put the info in a regular list
            subjects_list = [x['id'] for x in subjects_info]
            return subjects_list
        else:
            return None

    # Returns the amount of users that made this list
    def amountOfUsersWhoMadeThisList(self):
        return dbw.getAmountOfUsersWhoMadeList(self.id)['amount']

    # Returns the average of users' scores for this list
    def averageOfUsersForThisList(self):
        return dbw.getAvgScoreOfUsersWhoMadeList(self.id)['average']

    # Returns the average of users' ratings for this list
    def averageRatingOfUsersForThisList(self):
        ratings = dbw.averageRatingOfUsersWhoMadeList(self.id)
        total_rating = 0
        rating_divider = 0
        if ratings:
            for rating in ratings:
                # Ratings of 0 are not valid (default)
                if rating['rating'] != 0:
                    total_rating += rating['rating']
                    rating_divider += 1
            # no ratings yet
            if rating_divider == 0:
                return 0
            total_rating = total_rating / rating_divider
        return total_rating

    # Returns the amount of exercises in this list
    def amountOfExercises(self):
        return len(self.allExercises('en'))

    # List of Exercise-objects that belong to this list (original and references)
    def allExercises(self, language_code):
        # we'll need to check if any numbers are missing, so we get the amount of em
        # Getting all original exercise_ids
        exercises_infos = dbw.getExercisesForList(self.id)
        # Getting all references
        exercise_references_infos = dbw.getExerciseReferencesForList(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        exercises = []
        # We'll put the info in a regular list
        # The normal exercises
        for exercise_id in exercises_infos:
            exercises.append(object_manager.createExercise(exercise_id['id'], language_code))
        # The references
        for exercise_id in exercise_references_infos:
            referenced = object_manager.createExercise(exercise_id['id'], language_code)
            referenced.exercise_number = exercise_id['new_list_exercise_number']
            referenced.exerciseList_id = self.id
            referenced.isReference = True
            exercises.append(referenced)
        # now we sort the exercises on exercise_number
        exercises = sorted(exercises, key=lambda ex: ex.exercise_number)
        return exercises

    # Gets one specific exercise belonging to this list on the id
    def getExercise(self, id, language_code):
        for ex in allExercises(language_code):
            if ex.id == id:
                return ex
            else:
                return None

    # Returns specific variables depending on what was asked
    def hasX(self, id, X_type):
        if X_type == 'Subject':
            return self.hasSubject(id)
        elif X_type == 'Programming Language':
            return self.programming_language.id == id

    # Checks whether the exerciselist has a certain subject
    def hasSubject(self, subject_id):
        subjects_info = dbw.getSubjectIDsForList(self.id)
        if subjects_info:
            # We'll put the info in a regular list
            subjects_list = [x['id'] for x in subjects_info]
            return subject_id in subjects_list

    # Updates the database to the variables on the current object
    def save(self):
        dbw.updateExerciseList(self.id, self.name, self.description, self.difficulty, self.programming_language)

    # Updates the current object+ the database
    def update(self, updated_name, updated_description, updated_difficulty, updated_prog_lang, translation=None):
        dbw.updateExerciseList(self.id, updated_name, updated_description, updated_difficulty, updated_prog_lang.id, translation)
        self.name = updated_name
        self.description = updated_description
        self.difficulty = int(updated_difficulty)
        self.programming_language = updated_prog_lang

    # Adds a subject for this list to the database
    def addSubject(self, subject_name):
        dbw.insertSubject(subject_name)
        subject_id = int(dbw.getSubjectID(subject_name)["id"])
        dbw.insertHasSubject(self.id, subject_id)

    # Deletes a subject from this list in the database
    def deleteSubject(self, subject_name):
        subject_id = int(dbw.getSubjectID(subject_name)["id"])
        dbw.deleteSubjectFromHasSubject(self.id, subject_id)

    # Gets the exercises of this list that a user has made or attempted
    def getAllExercForUserForList(self, user_id):
        return dbw.getAllExercForUserForList(user_id, self.id)

    # Inserts a new exercise into the list (and database)
    # (this info is spread out over multiple tables)
    def insertExercise(self, max_score, penalty, exercise_type, created_by, created_on, exercise_number, question, answers, correct_answer, hints, language_obj, title, translation, code=""):
        # AssociatedWith relation
        l_id = language_obj.id
        # Info for exercises table + id of the exercise
        exercise_id = dbw.insertExercise(max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, self.id, title, l_id)['highest_id']
        if exercise_type == "Code" or exercise_type == "Turtle":
            dbw.insertCode(code, exercise_id)
        # question is een QuestionContainer object
        dbw.insertQuestion(exercise_id, question.language.id, question.question_text)

        import managers.om.objectmanager
        object_manager = managers.om.objectmanager.ObjectManager()

        for i, answer in enumerate(answers):
            if exercise_type == "Open Question":
                dbw.insertAnswer(exercise_id, language_obj.id, i + 1, answer)
            else:
                dbw.insertAnswer(exercise_id, 1, i + 1, answer)

        for i, hint in enumerate(hints):
            dbw.insertHint(exercise_id, l_id, i + 1, hint)

        exercise = object_manager.createExercise(exercise_id, language_obj.code)

        exercise.update(correct_answer, answers, hints, language_obj)
        exercise.setTranslations(translation)

    # Gets the numerically last exercise of this list
    def getLastExercise(self):
        last = dbw.getLastExerciseFromList(self.id)["last_exercise_number"]
        if last is None:
            return 0
        else:
            return last

    # Inserts a reference to an exercise in this list
    def insertExerciseByReference(self, original_exercise_id):
        new_list_exercise_number = int(self.getLastExercise()) + 1
        dbw.insertExerciseByReference(original_exercise_id, self.id, new_list_exercise_number)
        return new_list_exercise_number

    # Makes a reference into its own unique exercise
    def unreferenceExercise(self, exercise_number):
        # to 'unreference' something, we have to add it to the DB
        object_manager = managers.om.objectmanager.ObjectManager()
        # first, we'll have to look up what the original exercise was
        original_ex_id = int(dbw.getOriginalExercise(self.id, exercise_number)['id'])
        new_id = dbw.copyExercise(original_ex_id, exercise_number, self.id)
        # now we need to delete the reference from the DB
        dbw.deleteReference(self.id, exercise_number)
        return new_id

    # Make a new exercise based on another one
    def copyExercise(self, original_exercise_id):
        number = self.insertExerciseByReference(original_exercise_id)
        self.unreferenceExercise(number)

    # TODO
    def maxScore(self):
        return dbw.getMaxSumForExForList(self.id) + dbw.getMaxSumForRefForList(self.id)

    # TODO
    def fixUpdateNumbers(self, exercises, pos_change):
        nextPos = len(exercises) + 1
        # check if there are exercises who might cause problems
        # The only exercises who can cause problems are the

        transaction = ""
        after_transaction = ""
        for i, ex in enumerate(exercises):
            if pos_change[i] == 0:
                # If we did not change pos -> no prob!
                transaction += ex.saveExerciseNumber(i + 1)

            else:
                # Get the exercise on our current spot!
                distance = pos_change[i]
                ex_on_new_place = exercises[ex.exercise_number + distance - 1]
                if ex.id == ex_on_new_place.id:
                    # Ow problem! The exercise on our new spot has the same id...
                    # fix this with putting us behind the list
                    transaction += ex.saveExerciseNumber(nextPos)
                    nextPos += 1
                    after_transaction += ex.saveExerciseNumber(i + 1)
                else:
                    transaction += ex.saveExerciseNumber(i + 1)

        return transaction + after_transaction

    # scrambled_exercises is a list of Exercise objects
    def reorderExercises(self, scrambled_exercise_ids, language_code):
        # First we need to convert the list of integers to actual objects
        normal_order = self.allExercises(language_code)
        scrambled_exercises = []
        pos_change = []
        remove = []
        last_exercise = self.getLastExercise()
        for i in range(1, last_exercise + 1):
            if i not in scrambled_exercise_ids:
                scrambled_exercise_ids.append(i)
                remove.append(i)

        for i, ex_number in enumerate(scrambled_exercise_ids):
            for j, ex in enumerate(normal_order):
                if ex.exercise_number == ex_number:
                    scrambled_exercises.append(ex)
                    pos_change.append(i - j)
                    break

        # First we'll check which exercises were deleted
        # The amount of exercises we had at first
        transaction = self.fixUpdateNumbers(scrambled_exercises, pos_change)
        dbw.UpdateExerciseAndReferenceNumbers(transaction)

        for i in range(len(remove)):
            self.deleteExercise(last_exercise - i)

    # Removes an exercise of reference to an exercise in this list
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
                exercise_list = object_manager.createExerciseList(reference['list_id'], 1)
                exercise_list.unreferenceExercise(reference['exercise_number'])
            # Now we'll delete the old exercise
            dbw.deleteExercise(exercise.id)

    # TODO
    def searchString(self):
        return str(self.name)

    # Gets the translations of the title/description/... for this list
    def getAllTranslations(self):
        transl = dbw.getAllListTranslations(self.id)
        translations = {}
        object_manager = managers.om.objectmanager.ObjectManager()
        for val in transl:
            translations[object_manager.getLanguageObject(val['language_code']).name] = {'name': val['name'], 'description': val['description'].decode('ascii')}
        return translations

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

import dbw
import managers.om.exercise

class ExerciseList:
    def __init__(self,id,name,difficulty,description, created_by, created_on, programming_lang):
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.description = description
        self.created_by = created_by
        self.created_on = created_on
        self.programming_language = programming_lang
        self.programming_language_string = dbw.getNameFromProgLangID(programming_lang)['name']

    def __str__(self):
        return self.name+' '+str(self.difficulty)+' '+self.description +' '+ str(self.created_by) + ' ' + str(self.created_on)

    # List of subjects
    def allSubjects(self):
        subjects_info = dbw.getSubjectsForList(self.id)
        if subjects_info:
            # We'll put the info in a regular list
            subjects_list = [ x['name'] for x in subjects_info]
            return subjects_list
        else:
            return None

    # List of exercises
    def allExercises(self, language_code):
        exercises_infos = dbw.getExercisesForList(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        exercises = []
        if exercises_infos:
            # We'll put the info in a regular list
            exercises = []
            for exercise_id in exercises_infos:
                exercises.append(object_manager.createExercise(exercise_id['id'],language_code))
            return exercises
        else:
            return None

    def save(self):
        dbw.updateExerciseList(self.id,self.name, self.description ,self.difficulty, self.programming_language)

#TODO: how to add subjects

    def addSubject(self, subject_name):
        dbw.insertSubject(subject_name)
        subject_id = int(dbw.getSubjectID(subject_name)["id"])

        dbw.insertHasSubject(self.id, subject_id)

    def deleteSubject(self, subject_name):
        subject_id = int(dbw.getSubjectID(subject_name)["id"])
        dbw.deleteSubjectFromHasSubject(self.id, subject_id)


    def insertExercise(self,difficulty, max_score, penalty, exercise_type,created_by
        , created_on, exercise_number,question,answers,correct_answer
        ,hints,language_code,title,code = ""):
        # Info for exercises table + id of the exercise
        exercise_id = dbw.insertExercise(difficulty, max_score, penalty, exercise_type
        ,created_by, created_on, exercise_number,correct_answer,self.id, title)['highest_id']
        # AssociatedWith relation
        l_id = dbw.getIdFromLanguage(language_code)['id']
        # Code (default "")
        if(code != ""):
            dbw.insertCode(code,exercise_id)
        # question = QuestionContainer object
        dbw.insertQuestion(question.question_text, question.language_id, exercise_id)

        import managers.om.objectmanager
        object_manager = managers.om.objectmanager.ObjectManager()

        for i, answer in enumerate(answers):
            dbw.insertAnswer(i+1, answer, 1, exercise_id)

        for i, hint in enumerate(hints):
            dbw.insertHint(hint, i+1, exercise_id,l_id)

        exercise = object_manager.createExercise(exercise_id, language_code)

        exercise.update(correct_answer,answers,hints)


    def getLastExercise(self):
        if dbw.getLastExerciseFromList(self.id)["last_exercise_number"] == None:
            return 0
        else:
           return dbw.getLastExerciseFromList(self.id)["last_exercise_number"]

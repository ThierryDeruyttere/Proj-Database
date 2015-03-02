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
    def allExercises(self,language_code):
        exercises_infos = dbw.getExercisesForList(self.id)
        if exercises_infos:
            # We'll put the info in a regular list
            exercises = []
            for exercise_id in exercises_infos:
                exercise_info = dbw.getExerciseInformation(exercise_id['id'],language_code)
                exercise_object = managers.om.exercise.Exercise(self.id,exercise_info['difficulty'],
                exercise_info['max_score'],exercise_info['penalty'],exercise_info['exercise_type']
                ,exercise_info['programming_language'],exercise_info['code_text'],exercise_info['question_text']
                ,language_code,exercise_info['answer_text'],exercise_info['language_name'])
                exercises.append(exercise_object)
            return exercises
        else:
            return None

    def save(self):
        dbw.updateExerciseList(self.id,self.name, self.description ,self.difficulty, self.programming_language)

#TODO: how to add subjects

    def addSubject(self):
        pass

    def deleteSubject(self):
        pass

    def insertExercise(self,difficulty, max_score, penalty, exercise_type,created_by
        , created_on, exercise_number,programming_language,question,answers,correct_answer
        ,hints,language_code,code = ""):
        # Info for exercises table + id of the exercise
        exercise_id = dbw.insertExercise(difficulty, max_score, penalty, exercise_type
        ,created_by, created_on, exercise_number,correct_answer,self.id)['highest_id']
        # AssociatedWith relation
        l_id = dbw.getIdFromLanguageCode(language_code)['id']
        # Code (default "")
        dbw.insertCode(code,exercise_id)
        # question = QuestionContainer object
        dbw.insertQuestion(question.question_text, question.language_id, exercise_id)
        import managers.om.objectmanager
        object_manager = objectmanager.ObjectManager()
        exercise = object_manager.createExercise(exercise_id)
        exercise.update(correct_answer,answers,hints)

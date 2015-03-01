import dbw
import om.exercise

class ExerciseList:
    def __init__(self,id,name,difficulty,description, created_by, created_on, programming_lang):
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.description = description
        self.created_by = created_by
        self.created_on = created_on
        self.programming_language = programming_lang

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
                exercise_object = om.exercise.Exercise(self.id,exercise_info['difficulty'],
                exercise_info['max_score'],exercise_info['penalty'],exercise_info['exercise_type']
                ,exercise_info['programming_language'],exercise_info['code_text'],exercise_info['question_text']
                ,language_code,exercise_info['answer_text'],exercise_info['language_name'])
                exercises.append(exercise_object)
            return exercises
        else:
            return None

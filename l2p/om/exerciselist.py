class ExerciseList:
    def __init__(self,id,name,difficulty,description):
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.description = description

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
        def allExercises(self):
            exercises_info = dbw.getExercisesForList(self.id)
            if exercises_info:
                # We'll put the info in a regular list
                exercises_list = [ x['exercise_id'] for x in exercises_info]
                return exercises_list
            else:
                return None


from managers.om import *
object_manager = objectmanager.ObjectManager()

class StatisticsAnalyzer:
    '''Class that will use the om to query+analyze data (and put it into proper formats
    for the graphmanager to use?)'''
    def __init__(self):
        pass

# Used with Pie Graphs

    # returns a dict consisting of the "labels"=languages and "data" = # of exercises
    def AmountOfExerciseListsPerProgrammingLanguage(self):
        result = {}
        all_prog_languages = object_manager.allProgrammingLanguages()
        languages = []
        amount_of_exercises = []
        for prog_lang in all_prog_languages:
            count = object_manager.countExerciseListsForProgrammingLanguageID(prog_lang['id'])
            languages.append(prog_lang['name'])
            amount_of_exercises.append(count['amount'])
        result['labels'] = languages
        result['data'] = amount_of_exercises
        return result

# Used with Bar Charts

# Used with Line Graphs

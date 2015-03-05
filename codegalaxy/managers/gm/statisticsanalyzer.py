
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

    # Return the X biggest groups
    def BiggestGroupsTopX(self,X):
        result = {}
        result['labels'] = []
        result['data'] = []
        result['data'].append([])
        groups = object_manager.allGroups()
        groups.sort(key=lambda x: len(x.allMembers()), reverse=True)
        groups = groups[:X]
        for i in range(X):
            result['data'][0].append(len(groups[i].allMembers()))
            result['labels'].append(groups[i].group_name)
        return result
        
# Used with Line Graphs

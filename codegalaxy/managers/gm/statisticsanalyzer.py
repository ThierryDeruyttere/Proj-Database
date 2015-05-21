
from managers.om import *
object_manager = objectmanager.ObjectManager()

class StatisticsAnalyzer:

    '''Class that will use the om to query+analyze data (and put it into
    proper formats for the graphmanager to use)'''

    def __init__(self):
        pass

# Used with Pie Graphs

    # returns a dict consisting of the "labels"=languages and "data" = # of exercises
    def AmountOfExerciseListsPerProgrammingLanguage(self):
        result = {}
        # Programming language names
        result['labels'] = []
        # amount of exercises
        result['data'] = []
        all_prog_languages = object_manager.allProgrammingLanguages()
        for prog_lang in all_prog_languages:
            count = object_manager.countExerciseListsForProgrammingLanguageID(prog_lang['id'])
            set_item = False
            # ordering from small to large
            for i in range(len(result['data']) - 1):
                if result['data'][i] >= count['amount']:
                    result['labels'].insert(i, prog_lang['name'])
                    result['data'].insert(i, count['amount'])
                    set_item = True
            if not set_item:
                result['labels'].append(prog_lang['name'])
                result['data'].append(count['amount'])
        result['labels'].reverse()
        result['data'].reverse()
        return result

    def AmountOfExercisesPerProgrammingLanguageForUser(self, user_id):
        result = {}
        # Programming language names
        result['labels'] = []
        # amount of exercises
        result['data'] = []
        all_prog_languages = object_manager.allProgrammingLanguages()
        for prog_lang in all_prog_languages:
            count = object_manager.countExercisesForProgrammingLanguageIDMadeByUser(prog_lang['id'], user_id)
            set_item = False
            # ordering from small to large
            for i in range(len(result['data']) - 1):
                if result['data'][i] >= count['amount']:
                    result['labels'].insert(i, prog_lang['name'])
                    result['data'].insert(i, count['amount'])
                    set_item = True
            if not set_item:
                result['labels'].append(prog_lang['name'])
                result['data'].append(count['amount'])
        result['labels'].reverse()
        result['data'].reverse()
        return result

    def AmountOfExerciseListsPerProgrammingLanguageForUser(self, user_id):
        result = {}
        # Programming language names
        result['labels'] = []
        # amount of exercises
        result['data'] = []
        all_prog_languages = object_manager.allProgrammingLanguages()
        for prog_lang in all_prog_languages:
            count = object_manager.countExerciseListsForProgrammingLanguageIDMadeByUser(prog_lang['id'], user_id)
            set_item = False
            # ordering from small to large
            for i in range(len(result['data']) - 1):
                if result['data'][i] >= count['amount']:
                    result['labels'].insert(i, prog_lang['name'])
                    result['data'].insert(i, count['amount'])
                    set_item = True
            if not set_item:
                result['labels'].append(prog_lang['name'])
                result['data'].append(count['amount'])
        result['labels'].reverse()
        result['data'].reverse()
        return result

# Used with Bar Charts

    def averageScorePerProgrammingLanguageForUser(self, user):
        result = {}
        # programming language_ids
        result['labels'] = []
        # score per language
        result['data'] = []
        result['data'].append([])
        all_prog_languages = object_manager.allProgrammingLanguages()
        for i in range(len(all_prog_languages)):
            if user.averageScoreForProgrammingLanguage(all_prog_languages[i]['id']):
                result['data'][0].append(user.averageScoreForProgrammingLanguage(all_prog_languages[i]['id']))
                result['labels'].append(all_prog_languages[i]['name'])
        return result

    # Return the X biggest groups
    def biggestGroupsTopX(self, X):
        result = {}
        # Names of groups
        result['labels'] = []
        # amount of members
        result['data'] = []
        result['data'].append([])
        groups = object_manager.allGroups()
        groups.sort(key=lambda x: len(x.allMembers()), reverse=True)
        if(X < len(groups)):
            groups = groups[:X]
        for i in range(len(groups)):
            result['data'][0].append(len(groups[i].allMembers()))
            result['labels'].append(groups[i].group_name)
        return result

    def mostExerciseListsTopX(self, X):
        result = {}
        # Names of Users
        result['labels'] = []
        # Amount of exerciselists
        result['data'] = []
        result['data'].append([])
        users = object_manager.allUsers()
        users.sort(key=lambda x: len(x.allPersonalLists()), reverse=True)
        if(X < len(users)):
            users = users[:X]
        for i in range(len(users)):
            result['data'][0].append(len(users[i].allPersonalLists()))
            result['labels'].append(users[i].first_name + ' ' + users[i].last_name)
        return result

    def mostPopularSubjectsTopX(self, X):
        result = {}
        # Names of Users
        result['labels'] = []
        # Amount of exerciselists
        result['data'] = []
        result['data'].append([])
        subjects = object_manager.allSubjects()
        subjects_list = [(item['name'], object_manager.occurencesOfSubject(item['id'])['amount']) for item in subjects]
        subjects_list.sort(key=lambda x: x[1], reverse=True)
        if(X < len(subjects_list)):
            subjects_list = subjects_list[:X]
        for i in range(len(subjects_list)):
            result['data'][0].append(subjects_list[i][1])
            result['labels'].append(subjects_list[i][0])
        return result

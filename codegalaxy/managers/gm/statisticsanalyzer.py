
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
        # Programming language names
        result['labels'] = []
        # amount of exercises
        result['data'] = []
        all_prog_languages = object_manager.allProgrammingLanguages()
        for prog_lang in all_prog_languages:
            count = object_manager.countExerciseListsForProgrammingLanguageID(prog_lang['id'])
            result['labels'].append(prog_lang['name'])
            result['data'].append(count['amount'])
        return result

# Used with Bar Charts

    # Return the X biggest groups
    def biggestGroupsTopX(self,X):
        result = {}
        # Names of groups
        result['labels'] = []
        # amount of members
        result['data'] = []
        result['data'].append([])
        groups = object_manager.allGroups()
        groups.sort(key=lambda x: len(x.allMembers()), reverse=True)
        groups = groups[:X]
        for i in range(X):
            result['data'][0].append(len(groups[i].allMembers()))
            result['labels'].append(groups[i].group_name)
        return result

    def mostExerciseListsTopX(self,X):
        result = {}
        # Names of Users
        result['labels'] = []
        # Amount of exerciselists
        result['data'] = []
        result['data'].append([])
        users = object_manager.allUsers()
        users.sort(key=lambda x: len(x.allPersonalLists()), reverse=True)
        users = users[:X]
        for i in range(X):
            result['data'][0].append(len(users[i].allPersonalLists()))
            result['labels'].append(users[i].first_name+users[i].last_name)
        return result

    def compareUserExercisesPerProgrammingLanguageWithFriend(self,user_id,friend_id):
        result = {}
        # Names of languages
        result['labels'] = []
        # Amount of exercises
        result['data'] = []
        # User 0
        result['data'].append([])
        # Friend 1
        result['data'].append([])
        all_prog_languages = object_manager.allProgrammingLanguages()
        user = object_manager.createUser(id = user_id)
        friend = object_manager.createUser(id = friend_id)
        user_ex = user.allPersonalExercises()
        friend_ex = friend.allPersonalExercises()
        #allPersonalExercises
        for prog_lang in all_prog_languages:
            result['labels'].append(prog_lang['name'])
            user_count = 0
            for ex in user_ex :
                if ex['name'] == prog_lang['name']:
                    user_count += 1
            result['data'][0].append([user_count])
            friend_count = 0
            for ex in friend_ex :
                if ex['name'] == prog_lang['name']:
                    friend_count += 1
            result['data'][1].append([friend_count])
        return result

    #WIP
    def mostPopularSubjectsTopX(self,X):
        result = {}
        # Names of Users
        result['labels'] = []
        # Amount of exerciselists
        result['data'] = []
        result['data'].append([])
        subjects = object_manager.allSubjects()
        subjects_list = [(item['name'],object_manager.occurencesOfSubject(item['id'])['amount']) for item in subjects]
        subjects_list.sort(key=lambda x: x[1], reverse=True)
        subjects_list = subjects_list[:X]
        for i in range(X):
            result['data'][0].append(subjects_list[i][1])
            result['labels'].append(subjects_list[i][0])
        return result

# Used with Line Graphs

import om.exerciselist
import om.exercise
import om.group
import dbw

class User:
    def __init__(self,id,first_name,last_name,is_active,email,permissions,password):
        # Plain info on the user
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.email = email
        self.permissions = permissions
        self.password = password


    # List with other users this user is befriended with
    def allFriends(self):
        friends_info = dbw.getFriendsIdForID(self.id)
        if friends_info:
            friends_list = []
            # We'll make objects of the friends and put them in a list
            for friend in friends_info:
                friend_info = dbw.getUserOnId(friend['friend_id'])
                if friend_info:
                    # If the info is legit, we add a User object with the info to the list
                    friend_object = User(friend['friend_id'],friend_info['first_name'],friend_info['last_name'],
                    friend_info['is_active'],friend_info['email'],friend_info['permission'],friend_info['password'])
                    friends_list.append(friend_object)
            return friends_list
        else:
            return None

    # List with all the groups this user is currently in (SQL function)
    def allGroups(self):
        groups_info = dbw.getGroupsFromUser(self.id)
        if groups_info:
            groups_list = []
            # We'll make objects of the friends and put them in a list
            for group in groups_info:
                group_info = dbw.getGroupInformation(group['group_id'])
                if group_info:
                    # If the info is legit, we add a Group object with the info to the list
                    group_object = om.group.Group(group['group_id'],group_info['group_name'],group_info['group_type'])
                    groups_list.append(group_object)
            return groups_list
        else:
            return None

    # List with all the lists of exercises this user has completed/is working on (SQL function)
    def allPersonalLists(self):
        exercises_lists_info = dbw.getMadeListForUser(self.id)
        if exercises_lists_info:
            exercises_lists_list = []
            # We'll make objects of the friends and put them in a list
            for exercises_list in exercises_lists_info:
                # If the info is legit, we add a User object with the info to the list
                exercises_list_object = PersonalList(exercises_list['rating'],exercises_list['score']
                ,exercises_list['exerciseList_id'],self.id)
                exercises_lists_list.append(exercises_list_object)
            return exercises_lists_list
        else:
            return None

    # returns TRUE for admin and FALSE for regular user
    def checkPermission(self,group_id):
        permissions_info = dbw.getPermForUserInGroup(self.id,group_id)
        if permissions_info:
            if permissions_info['user_permissions']:
                return True
            else:
                return False
        else:
            return None

    def save(self):
        dbw.updateUser(self.id,self.first_name,self.last_name
        ,self.password,self.email,self.is_active,self.permissions)

    def __str__(self):
         return str(self.id)+' '+self.first_name+' '+self.last_name+'\n'+str(self.is_active)+'\n'+self.email+'\n'+str(self.permissions)

class PersonalList:
    def __init__(self,rating,score,exercise_list_id,user_id):
        #given rating
        self.rating = rating
        # total obtained score
        self.score = score
        # Needed to use the allExercises function
        self.user_id = user_id
        exercise_list_info = dbw.getExerciseListInformation(exercise_list_id)
        exercise_list_object = om.exerciselist.ExerciseList(exercise_list_id,exercise_list_info['name'],
        exercise_list_info['difficulty'],exercise_list_info['description'],exercise_list_info['created_by']
        ,exercise_list_info['created_on'],exercise_list_info['prog_lang_id'])
        # Actual exercises-object (make with SQL queries)
        self.exercises_list = exercise_list_object
        # Integer representing the number of the last-made excersise (needed?) ('calculate' with the real list-obj)
        # self.last_made = None

    # Object which represents the actual list of personal exercises (SQL function)
    def allExercises(self):
        exercise_info = dbw.getExerciseScoreFor(self.user_id,self.exercises_list.id)
        if exercise_info:
            personal_exercises_list = [PersonalExercise(x['solved'],x['exercise_score'],x['rating'],x['exercise_id']) for x in exercise_info]
            return personal_exercises_list
        else:
            return None

    def __str__(self):
         return str(self.rating)+' '+str(self.score)+' '+str(self.user_id)+' '+self.exercises_list.name+' '+str(self.exercises_list.difficulty)+' '+self.exercises_list.description

class PersonalExercise:
    def __init__(self,solved,score,rating,exercise_id):
        # bool to check if exercise was solved
        self.solved = solved
        # obtained score
        self.score = score
        # given rating
        self.rating = rating

        exercise_info = dbw.getExerciseInformation(exercise_id)
        # Actual exercises-object (make with SQL queries)
        self.exercise = om.exercise.Exercise(exercise_id,exercise_info['difficulty'],
        exercise_info['max_score'],exercise_info['penalty'],exercise_info['exercise_type']
        ,exercise_info['programming_language'],exercise_info['code_text'],exercise_info['question_text']
        ,exercise_info['language_code'],exercise_info['answer_text'],exercise_info['language_name'])


    def __str__(self):
         return str(self.rating)+" "+str(self.score)+" "+str(self.solved)+" "+str(self.exercise)

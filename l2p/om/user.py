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
                friend_info = dbw.getUserOnId(friend["friend_id"])[0]
                if friend_info:
                    # If the info is legit, we add a User object with the info to the list
                    friend_object = User(friend["friend_id"],friend_info["first_name"],friend_info["last_name"],
                    friend_info["is_active"],friend_info["email"],friend_info["permission"],friend_info['password'])
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
                group_info = dbw.getGroupInformation(group["group_id"])[0]
                if group_info:
                    # If the info is legit, we add a User object with the info to the list
                    group_object = om.group.Group(group["group_id"],group_info["group_name"],group_info["group_type"])
                    groups_list.append(group_object)
            return groups_list
        else:
            return None

    # List with all the lists of exercises this user has completed/is working on (SQL function)
    def allPersonalLists(self):
        lists_info = dbw.getMadeListForUser(self.id)
        if lists_info:
            personal_lists_list = [PersonalList(x["rating"],x["score"],x["exerciseList_id"],self.id) for x in lists_info]
            return personal_lists_list
        else:
            return None

    # returns TRUE for admin and FALSE for regular user
    def checkPermission(self,group_id):
        permissions_info = dbw.getPermForUserInGroup(self.id,group_id)
        if permissions_info:
            # What to check for? TODO
            if permissions_info[user_permissions]:
                return True
            else:
                return False
        else:
            return None

    def __str__(self):
         return str(self.id)+" "+self.first_name+" "+self.last_name+"\n"+str(self.is_active)+"\n"+self.email+"\n"+str(self.permissions)

class PersonalList:
    def __init__(self,rating,score,exercise_list_id,user_id):
        #given rating
        self.rating = rating
        # total obtained score
        self.score = score
        # Needed to use the allExercises function
        self.user_id = user_id
        # Actual exercises-object (make with SQL queries)
        self.excersises_list
        # Integer representing the number of the last-made excersise (needed?) ("calculate" with the real list-obj)
        self.last_made

        # Object which represents the actual list of personal exercises (SQL function)
        def allExercises(self,user_id):
            exercise_info = dbw.getExerciseScoreFor(self.id)
            if exercise_info:
                personal_exercises_list = [PersonalExercise(x["solved"],x["exercise_score"],x["rating"],x["exercise_id"],self.id) for x in exercise_info]
                return personal_exercises_list
            else:
                return None



class PersonalExercise:
    def __init__(self,solved,score,rating,exercise_id):
        # bool to check if exercise was solved
        self.solved = solved
        # obtained score
        self.score = score
        # given rating
        self.rating = rating
        # Object which represents the actual excersise (make with SQL query)
        self.excersise

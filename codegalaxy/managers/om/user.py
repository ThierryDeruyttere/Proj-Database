import managers.om.exerciselist
import managers.om.exercise
import managers.om.group
import managers.om.objectmanager
import dbw

class User:

    def __init__(self, id, first_name, last_name, is_active, email, permissions, password, joined_on, last_login, gender):
        # Plain info on the user
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.email = email
        self.permissions = permissions
        self.password = password
        self.joined_on = joined_on
        self.last_login = last_login
        self.gender = gender

    # List with other users this user is befriended with
    def allFriends(self):
        friends_info = dbw.getFriendsIdForID(self.id)
        friends_list = []
        object_manager = managers.om.objectmanager.ObjectManager()
        # We'll make objects of the friends and put them in a list
        for friend in friends_info:
            friends_list.append(object_manager.createUser(id=friend['friend_id']))
        return friends_list

    def allFriendships(self):
        friendship_info = dbw.getFriendshipsForID(self.id)
        accepted_friendship = []
        for friendship in friendship_info:
            if friendship['status'] == 'Friends':
                friendship.update({'type': 'friendship'})
                friendship.update({'datetime': friendship['befriended_on']})
                accepted_friendship.append(friendship)
        return accepted_friendship

    def isFriend(self, friend):
        '''
        @brief Check if a User is a friend of this user
        @param friend The User to be checked if this User is friends with
        @return True if the users are friends, False otherwise
        '''
        return friend.id in [f.id for f in self.allFriends()]

    def addFriend(self, friend):
        '''
        @brief Add a friend of this User
        '''
        if not self.isFriend(friend):
            dbw.insertFriendsWith(self.id, friend.id, 'Friends')

    # List with all the groups this user is currently in (SQL function)
    def allGroups(self):
        groups_info = dbw.getGroupsFromUser(self.id)
        groups_list = []
        object_manager = managers.om.objectmanager.ObjectManager()
        # We'll make objects of the friends and put them in a list
        for group in groups_info:
            # If the info is legit, we add a Group object with the info to the list
            groups_list.append(object_manager.createGroup(group['group_id']))
        return groups_list

    def allPendingFriendships(self):
        pending_friendships = dbw.getPendingFriendships(self.id)


        return pending_friendships

    def allUserAdded(self):
        group_members = dbw.getGroupsMemberOf(self.id)

        for group_member in group_members:
            group_member.update({'type': 'group_member'})
            group_member.update({'datetime': group_member['joined_on']})

        return group_members


    # List with all the lists of exercises this user has completed/is working on (SQL function)
    def allPersonalLists(self):
        exercises_lists_info = dbw.getMadeListForUser(self.id)
        exercises_lists_list = []
        # We'll make objects of the friends and put them in a list
        for exercises_list in exercises_lists_info:
            # If the info is legit, we add a User object with the info to the list
            exercises_list_object = PersonalList(exercises_list['rating'], exercises_list['score'], exercises_list['exerciseList_id'], self.id)
            exercises_lists_list.append(exercises_list_object)
        return exercises_lists_list


    def allExerciseListsMade(self):
        exercise_list_date = dbw.getMadeListForUser2(self.id)
        for exerciseList in exercise_list_date:
            exerciseList.update({'type': 'exerciseList'})
            exerciseList.update({'datetime': exerciseList['made_on']})
        return exercise_list_date


    # returns TRUE for admin and FALSE for regular user
    def checkPermission(self, group_id):
        permissions_info = dbw.getPermForUserInGroup(self.id, group_id)
        if permissions_info:
            if permissions_info['user_permissions']:
                return True
            else:
                return False
        else:
            return None

    def amountOfListsWithSubjectForUser(self, subject_id, dates, ratings):
        int amount_of_lists = dbw.amountOfListsWithSubjectForUser(subject_id, user_id)['amount']

    def ratingCounter(self, ratings, default):
        total_rating = 0
        illegit_lists = 0
        for rating in ratings:
            if rating['rating'] == 0:
                if default:
                    #default counts for 50%
                    total_rating += 2.5
                else:
                    #we need to count one less
                    illegit_lists += 1
            else:
                total_rating += rating['rating']
        return total_rating / (len(ratings) - illegit_lists)

    # average score on any subject
    def averageRating(self, default):
        ratings = dbw.listOfRatingsForUser(self.id)
        return ratingCounter(ratings, default)

    def subjectRating(self, subject_id):
        ratings = dbw.listOfRatingsForUserForSubject(self.id)
        return ratingCounter(ratings, default)

    def avgDate():
        pass

    def subjectDate():
        pass

    def save(self):
        dbw.updateUser(self.id, self.first_name, self.last_name, self.password, self.email, self.is_active, self.permissions, self.joined_on, self.last_login, self.gender)

    def __str__(self):
        return str(self.id) + ' ' + self.first_name + ' ' + self.last_name + ' ' + str(self.is_active) + ' ' + self.email + ' ' + str(self.permissions) + ' ' + str(self.joined_on) + ' ' + str(self.last_login) + ' ' + self.gender

class PersonalList:

    def __init__(self, rating, score, exercise_list_id, user_id):
        # given rating
        self.rating = rating
        # total obtained score
        self.score = score
        # Needed to use the allExercises function
        self.user_id = user_id
        # Actual exercises-object
        object_manager = managers.om.objectmanager.ObjectManager()
        self.exercises_list = object_manager.createExerciseList(exercise_list_id)
        # Integer representing the number of the last-made excersise (needed?) ('calculate' with the real list-obj)
        # self.last_made = None

    # Object which represents the actual list of personal exercises (SQL function)
    def allExercises(self, language_code):
        exercise_info = dbw.getExerciseScoreFor(self.user_id, self.exercises_list.id)
        if exercise_info:
            personal_exercises_list = [PersonalExercise(x['solved'], x['exercise_score'], x['rating'], x['exercise_id'], language_code, x['completed_on']) for x in exercise_info]
            return personal_exercises_list
        else:
            return None

    def __str__(self):
        return str(self.rating) + ' ' + str(self.score) + ' ' + str(self.user_id) + ' ' + self.exercises_list.name + ' ' + str(self.exercises_list.difficulty) + ' ' + self.exercises_list.description

class PersonalExercise:

    def __init__(self, solved, score, rating, exercise_id, language_code, completed_on):
        # bool to check if exercise was solved
        self.solved = solved
        # obtained score
        self.score = score
        # given rating
        self.rating = rating
        # completion date (first time)
        self.completed_on = completed_on
        # Actual exercises-object (make with SQL queries)
        object_manager = managers.om.objectmanager.ObjectManager()
        self.exercise = object_manager.createExercise(exercise_id, language_code)

    def __str__(self):
        return str(self.rating) + " " + str(self.score) + " " + str(self.solved) + " " + str(self.exercise) + ' ' + str(self.completed_on)

import managers.om.exerciselist
import managers.om.exercise
import managers.om.group
import managers.om.objectmanager
import dbw
import datetime
import time

from django.middleware import *
import os.path

class User:

    def __init__(self, id, first_name, last_name, is_active, email, permissions, password, joined_on, last_login, gender, badge):
        if not joined_on:
            raise ValueError("joined_on in user __init__ is None.")

        # Plain info on the user
        self.id = int(id)
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.email = email
        self.permissions = int(permissions)
        self.password = password
        self.joined_on = joined_on
        self.last_login = last_login
        self.gender = gender
        self.badge = badge

        if type(joined_on) is datetime.datetime:
            self.joined_on = str(joined_on.strftime("%Y-%m-%d %H:%M:%S"))

    def name(self):
        return self.first_name + ' ' + self.last_name

    def updateProfile(self, email, password):
        dbw.updateUserInformation(self.id, email, password)
        return True

    def getUserLists(self, lang_id):
        lists = dbw.getListsForUserId(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        # create Lists
        ex_lists = []
        for i in lists:
            ex_lists.append(object_manager.createExerciseList(i['id'], lang_id))
        return ex_lists

    def getAllExercisesCreated(self, lang_id):
        object_manager = managers.om.objectmanager.ObjectManager()
        user = object_manager.createUser(id=self.id)
        lists = dbw.getListsForUserId(self.id)

        exercise_lists_created = []

        for i in lists:
            exercise_list = object_manager.createExerciseList(i['id'], lang_id)
            created_exercise_list = managers.om.feed.CreatedExerciseList(user, exercise_list)
            exercise_lists_created.append(created_exercise_list)

        return exercise_lists_created

    def getPicture(self):
        profile_picture = "profile_pictures/{}.png".format(self.id)

        path = "./codegalaxy/static/" + profile_picture
        if os.path.isfile(path):
            profile_picture = profile_picture
        else:
            if self.gender == "M":
                profile_picture = "media/icons/male_user.png"
            elif self.gender == "F":
                profile_picture = "media/icons/female_user.png"
            else:
                profile_picture = "media/icons/unknown_user.png"
        return profile_picture

    def getAllRewards(self):
        object_manager = managers.om.objectmanager.ObjectManager()

        rewards = dbw.getAllRewards(self.id)
        reward_objects = {}
        gold = []
        silver = []
        bronze = []
        for reward in rewards:
            reward_object = object_manager.createBadge(reward['id'])
            if reward_object.medal == 'gold':
                gold.append(reward_object)
            elif reward_object.medal == 'silver':
                silver.append(reward_object)
            elif reward_object.medal == 'bronze':
                bronze.append(reward_object)
        reward_objects['gold'] = gold
        reward_objects['silver'] = silver
        reward_objects['bronze'] = bronze
        return reward_objects

    def getAllBadges(self):
        object_manager = managers.om.objectmanager.ObjectManager()

        rewards = dbw.getAllRewards(self.id)
        reward_objects = []

        for reward in rewards:
            reward_object = object_manager.createBadge(reward['id'])
            reward_objects.append(reward_object)

        return reward_objects

    # List with other users this user is befriended with
    def allFriends(self):
        object_manager = managers.om.objectmanager.ObjectManager()

        friendship_info = dbw.getFriendshipsForID(self.id)
        accepted_friends = []
        for friendship in friendship_info:
            if friendship['status'] == 'Friends':
                if friendship['user_id'] != self.id:
                    user = object_manager.createUser(id=self.id)
                    friend = object_manager.createUser(id=friendship['user_id'])
                    accepted_friends.append(friend)
                else:
                    user = object_manager.createUser(id=self.id)
                    friend = object_manager.createUser(id=friendship['friend_id'])
                    accepted_friends.append(friend)
        return accepted_friends

    def allFriendsNotMemberOfGroupWithID(self, group_id):
        friends_info = dbw.getFriendsNotMemberOfGroupWithID(self.id, group_id)
        friends_list = []
        object_manager = managers.om.objectmanager.ObjectManager()
        # We'll make objects of the friends and put them in a list
        for friend in friends_info:
            friends_list.append(
                object_manager.createUser(id=friend['id']))
        return friends_list

    def allFriendships(self):
        friendship_info = dbw.getFriendshipsForID(self.id)
        accepted_friendship = []
        for friendship in friendship_info:
            if friendship['status'] == 'Friends':
                friendship.update({'type': 'friendship'})
                friendship.update({'datetime': friendship['befriended_on']})
                friendship.update({'user_first_name': self.first_name})
                friendship.update({'user_last_name': self.last_name})
                friendship.update({'user_id': self.id})
                accepted_friendship.append(friendship)
        return accepted_friendship

    def allFriendsWith(self):
        object_manager = managers.om.objectmanager.ObjectManager()

        friendship_info = dbw.getFriendshipsForID(self.id)
        accepted_friendship = []
        for friendship in friendship_info:
            if friendship['status'] == 'Friends':
                if friendship['user_id'] != self.id:
                    user = object_manager.createUser(id=self.id)
                    friend = object_manager.createUser(id=friendship['user_id'])
                    friendship_object = managers.om.feed.FriendsWith(user, friend, friendship['befriended_on'], friendship['status'])
                    accepted_friendship.append(friendship_object)
                else:
                    user = object_manager.createUser(id=self.id)
                    friend = object_manager.createUser(id=friendship['friend_id'])
                    friendship_object = managers.om.feed.FriendsWith(user, friend, friendship['befriended_on'], friendship['status'])
                    accepted_friendship.append(friendship_object)
        return accepted_friendship

    def confirmFriendship(self, friend_id):
        dbw.incrementBadgeValue(self.id, 'hasFriend')
        dbw.incrementBadgeValue(friend_id, 'hasFriend')
        dbw.updateFriendship(self.id, friend_id)

    def declineFriendship(self, friend_id):
        dbw.deleteFriendship(self.id, friend_id)
        dbw.decrementBadgeValue(self.id, 'hasFriend')
        dbw.decrementBadgeValue(friend_id, 'hasFriend')

    def confirmGroupMembership(self, group_id):
        dbw.incrementBadgeValue(self.id, 'memberOfGroup')
        dbw.updateGroupMembership(self.id, group_id)

    def deleteGroupMembership(self, group_id):
        dbw.deleteGroupMembership(self.id, group_id)
        dbw.decrementBadgeValue(self.id, 'memberOfGroup')

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
            dbw.insertFriendsWith(self.id, friend.id, 'Pending')

    def removeFriend(self, friend):
        '''
        @brief Remove a friend of this User
        '''
        if self.isFriend(friend):
            dbw.deleteFriendship(self.id, friend.id)

    def isFriendshipPending(self, friend):
        pending_friendships = friend.allPendingFriendships2()
        pending_friendships2 = friend.allPeopleThatWantToAddMe()
        for pending_friendship in pending_friendships:
            if pending_friendship.user.id == friend.id:
                return True
            if pending_friendship.friend.id == self.id:
                return True
        for pending_friendship2 in pending_friendships2:
            if pending_friendship2.user.id == friend.id:
                return True
            if pending_friendship2.friend.id == self.id:
                return True

        return False

    # List with all the groups this user is currently in (SQL function)
    def allGroups(self):
        groups_info = dbw.getGroupsFromUser(self.id)
        groups_list = []
        object_manager = managers.om.objectmanager.ObjectManager()
        # We'll make objects of the friends and put them in a list
        for group in groups_info:
            if group['status'] == 'Member':
                # If the info is legit, we add a Group object with the info to the
                # list
                groups_list.append(object_manager.createGroup(group['group_id']))
        return groups_list

    def allPendingFriendships(self):
        pending_friendships = dbw.getPendingFriendships(self.id)
        return pending_friendships

    def allPendingFriendships2(self):
        pending_friendships = dbw.getPendingFriendships(self.id)

        object_manager = managers.om.objectmanager.ObjectManager()

        user = object_manager.createUser(id=self.id)

        pending_friendship_objects = []
        for pending_friendship in pending_friendships:
            friend = object_manager.createUser(id=pending_friendship['user_id'])

            friendship = managers.om.feed.FriendsWith(user, friend, pending_friendship['befriended_on'], pending_friendship['status'])
            pending_friendship_objects.append(friendship)
        return pending_friendship_objects

    def allPendingGroupMemberships(self):
        pending_group_membership = dbw.getPendingGroupMemberships(self.id)
        return pending_group_membership

    def allPendingGroupMemberships2(self):
        pending_group_memberships = dbw.getPendingGroupMemberships(self.id)

        object_manager = managers.om.objectmanager.ObjectManager()

        user = object_manager.createUser(id=self.id)

        pending_group_membership_objects = []

        for pending_group_membership in pending_group_memberships:
            group = object_manager.createGroup(pending_group_membership['group_id'])
            pending_group_membership_object = managers.om.feed.UserInGroup(group, user, pending_group_membership['user_permissions'], pending_group_membership['joined_on'], pending_group_membership['status'])
            pending_group_membership_objects.append(pending_group_membership_object)

        return pending_group_membership_objects

    def allPeopleThatWantToAddMe(self):
        pending_friendships = dbw.defGetReversePendingFriendships(self.id)

        object_manager = managers.om.objectmanager.ObjectManager()

        user = object_manager.createUser(id=self.id)

        pending_friendship_objects = []
        for pending_friendship in pending_friendships:
            friend = object_manager.createUser(id=pending_friendship['user_id'])

            friendship = managers.om.feed.FriendsWith(user, friend, pending_friendship['befriended_on'], pending_friendship['status'])
            pending_friendship_objects.append(friendship)
        return pending_friendship_objects

    def allUserAdded(self):
        group_members = dbw.getGroupsMemberOf(self.id)
        for group_member in group_members:
            group_member.update({'type': 'group_member'})
            group_member.update({'datetime': group_member['joined_on']})
            group_member.update({'user_first_name': self.first_name})
            group_member.update({'user_last_name': self.last_name})
            group_member.update({'user_id': self.id})
        return group_members

    def allGroupsJoined(self):
        object_manager = managers.om.objectmanager.ObjectManager()

        user = object_manager.createUser(id=self.id)

        groups_member_of = dbw.getGroupsMemberOf(self.id)

        user_in_groups = []
        for memberOf in groups_member_of:
            if memberOf['status'] == 'Member':
                group_object = object_manager.createGroup(memberOf['group_id'])
                user_in_group = managers.om.feed.UserInGroup(group_object, user, memberOf['user_permissions'], memberOf['joined_on'], memberOf['status'])
                user_in_groups.append(user_in_group)
        return user_in_groups

    def haveImadeList(self, list_id):
        for personal_list in self.allPersonalLists():
            if personal_list.exercises_list.id == list_id:
                return True
        return False

    def madeList(self, list_id, list_score, list_rating):
        if not self.haveImadeList(list_id):
            dbw.insertMadeList(list_id, self.id, list_rating, list_score)

    def updateListRating(self, list_id, list_rating):
        dbw.updateListRating(list_id, self.id, list_rating)

    # List with all the lists of exercises this user has completed/is working
    # on (SQL function)
    def allPersonalLists(self, lang_id=1):
        exercises_lists_info = dbw.getMadeListForUser(self.id)
        exercises_lists_list = []
        # We'll make objects of the friends and put them in a list
        for exercises_list in exercises_lists_info:
            # If the info is legit, we add a User object with the info to the
            # list
            exercises_list_object = PersonalList(exercises_list['rating'], exercises_list[
                                                 'score'], exercises_list['exerciseList_id'], self.id, exercises_list['made_on'], lang_id)
            exercises_lists_list.append(exercises_list_object)

        return exercises_lists_list

    def personalListWithId(self, list_id, lang_id):
        exercise_lists_info = dbw.getMadeListForUser(self.id)

        for exercise_list in exercise_lists_info:
            if exercise_list['exerciseList_id'] == list_id:
                exercise_list_object = PersonalList(exercise_list['rating'],
                                                    exercise_list['score'],
                                                    exercise_list['exerciseList_id'],
                                                    self.id,
                                                    exercise_list['made_on'],
                                                    lang_id)
                return exercise_list_object

    def shareExerciseListResult(self, list_id):
        dbw.updateSharedMadeExerciseList(self.id, list_id)

    def amountOfListsMade(self):
        lists = self.allPersonalLists()
        if not lists:
            return 0
        return len(lists)

    def amountOfGroupsJoined(self):
        groups = self.allGroupsJoined()
        if not groups:
            return 0
        return len(groups)

    def timeJoined(self):
        import datetime
        from dateutil.relativedelta import relativedelta
        now = datetime.datetime.now()
        date = datetime.datetime.strptime(self.joined_on, "%Y-%m-%d %H:%M:%S")
        return relativedelta(now, date)

    def timeJoinedString(self):
        time_joined = self.timeJoined()
        time_joined_string = ''
        if time_joined.years > 0:
            time_joined_string += str(time_joined.years) + ' year'
            if time_joined.years != 1:
                time_joined_string += 's'
            time_joined_string += ' '
        if time_joined.months > 0:
            time_joined_string += str(time_joined.months) + ' month'
            if time_joined.months != 1:
                time_joined_string += 's'
            time_joined_string += ' '
        if time_joined.days > 0:
            time_joined_string += str(time_joined.days) + ' day'
            if time_joined.days != 1:
                time_joined_string += 's'
            time_joined_string += ' '
        return time_joined_string

    def averageScoreOnLists(self):
        lists = self.allPersonalLists()
        if len(lists) == 0:
            return 0
        score = 0
        for made_list in lists:
            score += made_list.score
        return round(score / len(lists))

    def allExerciseListsShared(self, lang_id):
        object_manager = managers.om.objectmanager.ObjectManager()
        exercise_list_date = dbw.getMadeListForUser2(self.id)
        user = object_manager.createUser(id=self.id)
        all_exercise_lists_made = []
        for exercise_list in exercise_list_date:
            if exercise_list['shared'] == 1:
                exercise_list_object = object_manager.createExerciseList(exercise_list['exerciseList_id'], lang_id)
                made_exercise_list = managers.om.feed.MadeExerciseList(user, exercise_list_object, exercise_list['made_on'], lang_id)

                all_exercise_lists_made.append(made_exercise_list)

        return all_exercise_lists_made

    # List with all the exercises this user has completed
    def allPersonalExercises(self):
        prog_lang_ids = dbw.getProgrammingLanguageIDsOfMadeExForUser(self.id)
        real_names = []
        for prog_id in prog_lang_ids:
            real_names.append(
                dbw.getNameFromProgLangID(prog_id['prog_lang_id']))
        return real_names

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

    def ratingCounter(self, ratings, default):
        total_rating = 0
        illegit_lists = 0
        for rating in ratings:
            if rating['rating'] == 0:
                if default:
                    # default counts for 50%
                    total_rating += 2.5
                else:
                    # we need to count one less
                    illegit_lists += 1
            else:
                total_rating += rating['rating']
        if (len(ratings) - illegit_lists) > 0:
            return total_rating / (len(ratings) - illegit_lists)
        else:
            return 1

    # average score on any subject
    def averageRating(self, default):
        ratings = dbw.listOfRatingsForUser(self.id)
        return self.ratingCounter(ratings, default)

    def subjectRating(self, subject_id, default):
        ratings = dbw.listOfRatingsForUserForSubject(self.id, subject_id)
        return self.ratingCounter(ratings, default)

    def progLangRating(self, prog_lang_id, default):
        ratings = dbw.listOfRatingsForUserForProgrammingLanguage(
            self.id, prog_lang_id)
        return self.ratingCounter(ratings, default)

    def avgOfDates(self, dates):
        total_time = datetime.timedelta()
        for date in dates:
            total_time += managers.om.objectmanager.timeFromToday(
                date['made_on'])
        if len(dates) > 0:
            total_time /= len(dates)
            return -total_time
        else:
            return -total_time

    def avgDateAge(self):
        dates = dbw.listOfDatesForUser(self.id)
        return self.avgOfDates(dates)

    def avgSubjectDateAge(self, subject_id):
        dates = dbw.listOfDatesForUserForSubject(self.id, subject_id)
        return self.avgOfDates(dates)

    def avgProgrammingLanguageDateAge(self, prog_lang_id):
        dates = dbw.listOfDatesForUserForProgrammingLanguage(
            self.id, prog_lang_id)
        return self.avgOfDates(dates)

    def amountOfListsWithSubjectForUser(self, subject_id):
        return dbw.amountOfListsWithSubjectForUser(subject_id, self.id)['amount']

    def amountOfListsWithProgrammingLanguageForUser(self, prog_lang):
        return dbw.amountOfListsWithProgrammingLanguageForUser(prog_lang, self.id)['amount']

    def save(self):
        dbw.updateUser(self.id, self.first_name, self.last_name, self.password, self.email,
                       self.is_active, self.permissions, self.joined_on, self.last_login, self.gender)

    def getRatingForList(self, list_id):
        rating = dbw.getMadeListForUserForList(self.id, list_id)
        if rating is None:
            return 0
        return rating['rating']

    def __str__(self):
        return str(self.id) + ' ' + self.first_name + ' ' + self.last_name + ' ' + str(self.is_active) + ' ' + self.email + ' ' + str(self.permissions) + ' ' + str(self.joined_on) + ' ' + str(self.last_login) + ' ' + self.gender

    def getMadeList(self, list_id, lang_id):
        if list_id in [made_list.exercises_list.id for made_list in self.allPersonalLists(lang_id)]:
            return [made_list for made_list in self.allPersonalLists(lang_id) if list_id == made_list.exercises_list.id][0]
        return None

    def getLastAnswerForExercise(self, list_id, exercise_number):
        if dbw.getLastAnswerForExerciseForUser(self.id, list_id, exercise_number):
            if dbw.getLastAnswerForExerciseForUser(self.id, list_id, exercise_number)['last_answer']:
                return dbw.getLastAnswerForExerciseForUser(self.id, list_id, exercise_number)['last_answer']
        return 0

    def haveISolvedExercise(self, list_id, exercise_number):
        if dbw.hasUserSolvedExercise(list_id, exercise_number, self.id):
            return dbw.hasUserSolvedExercise(list_id, exercise_number, self.id)['solved']
        return False

    def latestHintIUsedForExercise(self, list_id, exercise_number):
        if dbw.latestHintUserUsedForExercise(list_id, exercise_number, self.id):
            if dbw.latestHintUserUsedForExercise(list_id, exercise_number, self.id)['hints_used']:
                return dbw.latestHintUserUsedForExercise(list_id, exercise_number, self.id)['hints_used']
        return 0

    def useHintForExercise(self, list_id, exercise_number, amount_of_hints, max_score, penalty):
        current_score = dbw.getScoreForExerciseForUser(self.id, list_id, exercise_number)
        previous_hint = self.latestHintIUsedForExercise(list_id, exercise_number)
        # If we can still ask for hints
        if int(amount_of_hints) > previous_hint:
            if dbw.userIsWorkingOn(list_id, exercise_number, self.id):
                dbw.userUsesHint(list_id, exercise_number, self.id, previous_hint + 1, current_score['exercise_score'] - penalty)
            else:
                object_manager = managers.om.objectmanager.ObjectManager()
                object_manager.userMadeExercise(self.id, max_score - penalty, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")), list_id, exercise_number, '', 1)
                object_manager.userMadeExercise(self.id, max_score - penalty, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")), list_id, exercise_number, '', 1)

    def searchString(self):
        return str(self.name())

    def searchResult(self, cur_user):

        mutual_friends = ' | '
        for cur_user_friend in cur_user.allFriends():
            for friend in self.allFriends():
                if cur_user_friend.id == friend.id:
                    mutual_friends += friend.name() + ' | '

        if len(mutual_friends) < 4:
            result = '''
            <div class="large-12 columns">
              <div class="panel radius">
                <div class="row">
                  <div class="large-3 columns">
                    <a href="/u/{id}">
                      <img src="/static/{picture}" class="round-image"/>
                    </a>
                  </div>
                  <div class="large-9 columns left">
                    <div class="row">
                      <a href="/u/{id}">
                        <h5 class="text-cut-off"><b>{name}</b></h5>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            '''.format(id=self.id, picture=self.getPicture(), name=self.name())

            return result

        result = '''
        <div class="large-12 columns">
          <div class="panel radius">
            <div class="row">
              <div class="large-3 columns">
                <a href="/u/{id}">
                  <img src="/static/{picture}" class="round-image"/>
                </a>
              </div>
              <div class="large-9 columns left">
                <div class="row">
                  <a href="/u/{id}">
                    <h5 class="text-cut-off"><b>{name}</b></h5>
                  </a>
                </div>
              </div>
              <br>
              <br>
              <br>
              <div class="row">
                <a href="/u/{id}">
                  <h6><b>Mutual friends:</b> {mut_friends}</h6>
                </a>
              </div>
            </div>
          </div>
        </div>
        '''.format(id=self.id, picture=self.getPicture(), name=self.name(), mut_friends=mutual_friends)

        return result

    def searchGroupResult(self, cur_user, group_id):
        result = '''
        <div class="large-12 columns">
          <div class="panel radius">
            <div class="row">
              <div class="large-3 columns">
                <a href="/u/{id}">
                  <img src="/static/{picture}" class="round-image"/>
                </a>
              </div>
              <div class="large-6 columns left">
                <div class="row">
                  <a href="/u/{id}">
                    <h5 class="text-cut-off"><b>{name}</b></h5>
                  </a>
                </div>
              </div>
              <div class="large-3 columns">
                <div id="u_{id}">
                  <a id="inviteuser" data-user_id="{id}" data-group_id="{group_id}" data-value><span class="mega-octicon octicon-plus"></span></a>
                </div>
              </div>
            </div>
          </div>
        </div>
        '''.format(id=self.id, picture=self.getPicture(), name=self.name(), group_id=group_id)
        return result

    def ownedLists(self):
        list_objects = []
        object_manager = managers.om.objectmanager.ObjectManager()
        list_ids = dbw.getExerciseListIdsMadeByUser(self.id)
        for list_id in list_ids:
            list_objects.append(object_manager.createExerciseList(list_id['id'], 1))
        return list_objects

    def averageScoreForProgrammingLanguage(self, prog_lang_id):
        return dbw.averageScoreForProgrammingLanguageForUser(prog_lang_id, self.id)['average']

    def sharedResult(self, exercise_list_id):
        shared_results = dbw.checkIfResultShared(self.id, exercise_list_id)

        if len(shared_results) == 0:
            return True
        else:
            return False

    def ratedExerciseList(self):
        dbw.incrementBadgeValue(self.id, 'gaveRating')

    def solvedExerciseList(self, creator_id):
        dbw.incrementBadgeValue(self.id, 'solvedList')

    def createdExerciseList(self):
        dbw.incrementBadgeValue(self.id, 'createdList')

    def createdGroup(self):
        dbw.incrementBadgeValue(self.id, 'createdGroup')

    def addDefaultBadges(self):
        dbw.insertDefaultBadges(self.id)

    def changeBadge(self, badge_name):
        dbw.changeBadge(self.id, badge_name)

    def checkTimeRelatedBadges(self):
        dbw.checkTimeRelatedBadges(self.id)


class PersonalList:

    def __init__(self, rating, score, exercise_list_id, user_id, made_on, language_id):
        # given rating
        self.rating = rating
        # total obtained score
        self.score = score
        # Needed to use the allExercises function
        self.user_id = user_id
        # Actual exercises-object
        object_manager = managers.om.objectmanager.ObjectManager()
        self.exercises_list = object_manager.createExerciseList(
            exercise_list_id, language_id)
        self.made_on = made_on
        # Integer representing the number of the last-made excersise (needed?) ('calculate' with the real list-obj)

    # Object which represents the actual list of personal exercises (SQL
    # function)
    def allExercises(self, language_code):
        exercise_info = dbw.getExerciseScoreFor(
            self.user_id, self.exercises_list.id)
        if exercise_info:
            personal_exercises_list = [PersonalExercise(x['solved'],
                                                        x['exercise_score'],
                                                        x['rating'],
                                                        x['exercise_id'],
                                                        language_code,
                                                        x['completed_on'],
                                                        self.exercises_list.id,
                                                        x['exercise_number']) for x in exercise_info]
            return personal_exercises_list
        else:
            return None

    def __str__(self):
        return str(self.score) + ' ' + str(self.user_id) + ' ' + self.exercises_list.name + ' ' + str(self.exercises_list.difficulty) + ' ' + self.exercises_list.description


class PersonalExercise:

    def __init__(self, solved, score, exercise_id, language_code, completed_on, list_id, exercise_number, last_answer):
        # bool to check if exercise was solved
        self.solved = solved
        # obtained score
        self.score = score
        # completion date (first time)
        self.completed_on = completed_on
        # Actual exercises-object (make with SQL queries)
        object_manager = managers.om.objectmanager.ObjectManager()
        self.exercise = object_manager.createExercise(
            exercise_id, language_code)
        self.list_id = list_id
        self.exercise_number = exercise_number
        self.last_answer = last_answer

    def __str__(self):
        return str(self.rating) + " " + str(self.score) + " " + str(self.solved) + " " + str(self.exercise) + ' ' + str(self.completed_on)

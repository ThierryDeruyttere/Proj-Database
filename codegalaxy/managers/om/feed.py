import managers.om.exerciselist
import managers.om.exercise
import managers.om.group
import managers.om.user
import managers.om.objectmanager
import dbw
import datetime

import os.path

# Feeditems die op de user en homepage komen
class FeedItem:

    def __init__(self, type, time_stamp):
        self.type = type
        self.datetime = time_stamp

    def __repr__(self):
        return str(self)

# Feeditem over user dat lid wordt van een groep
class UserInGroup(FeedItem):

    def __init__(self, group, user, user_permissions, joined_on, status):
        super().__init__('UserInGroup', joined_on)

        self.group = group
        self.user = user
        self.user_permissions = user_permissions
        self.joined_on = joined_on
        self.status = status

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' became member of ' + self.group.group_name + ' on ' + str(self.joined_on)

# Feeditem over user die een oefeningen lijst maakt
class MadeExerciseList(FeedItem):

    def __init__(self, user, exercise_list, completed_on, lang_id):
        super().__init__('MadeExerciseList', completed_on)

        self.user = user
        self.exercise_list = exercise_list
        self.personal_list = self.user.personalListWithId(self.exercise_list.id, lang_id)
        self.completed_on = completed_on

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' made: ' + self.exercise_list.name + ' on ' + str(self.completed_on)

# Feeditem over user die een nieuwe vriend heeft
class FriendsWith(FeedItem):

    def __init__(self, user, friend, befriended_on, status):
        super().__init__('FriendsWith', befriended_on)

        self.user = user
        self.friend = friend
        self.befriended_on = befriended_on
        self.status = status

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' became friends with: ' + self.friend.first_name + ' ' + self.friend.last_name + ' on ' + str(self.befriended_on)

# Feeditem over user die een oefeningen lijst aanmaakt
class CreatedExerciseList(FeedItem):

    def __init__(self, user, exercise_list):
        super().__init__('CreatedExerciseList', exercise_list.created_on)

        self.user = user
        self.exercise_list = exercise_list
        self.created_on = exercise_list.created_on

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' created ' + str(self.exercise_list.name) + ' on ' + str(self.created_on)

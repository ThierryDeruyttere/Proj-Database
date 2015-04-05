import managers.om.exerciselist
import managers.om.exercise
import managers.om.group
import managers.om.user
import managers.om.objectmanager
import dbw
import datetime

import os.path

class UserInGroup:
    def __init__(self, group, user, user_permissions, joined_on, status):
        self.group = group
        self.user = user
        self.user_permissions = user_permissions
        self.joined_on = joined_on
        self.status = status

        self.datetime = joined_on

        self.type = "UserInGroup"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' became member of ' + self.group.group_name + ' on ' + str(self.joined_on)

    def __repr__(self):
        return str(self)


class MadeExerciseList:
    def __init__(self, user, exercise_list, completed_on):
        self.user = user
        self.exercise_list = exercise_list
        self.completed_on = completed_on

        self.datetime = completed_on

        self.type = "MadeExerciseList"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' made: ' + self.exercise_list.name + ' on ' + str(self.completed_on)

    def __repr__(self):
        return str(self)

class FriendsWith:
    def __init__(self, user, friend, befriended_on, status):
        self.user = user
        self.friend = friend
        self.befriended_on = befriended_on
        self.status = status

        self.datetime = befriended_on

        self.type = "FriendsWith"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' became friends with: ' + self.friend.first_name + ' ' + self.friend.last_name + ' on ' + str(self.befriended_on)

    def __repr__(self):
        return str(self)

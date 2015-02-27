import hashlib
from om import *

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

object_manager = objectmanager.ObjectManager()

class CustomUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __init__(self,id,first_name,last_name,is_active,email,permissions,password):
        #Plain info on the user
        self.id = id
        #self.first_name = first_name
        #self.last_name = last_name
        #self.is_active = is_active
        self.email = email
        #self.permissions = permissions
        #self.password = password


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

    def __str__(self):
        return str(self.id)+' '+self.first_name+' '+self.last_name+'\n'+str(self.is_active)+'\n'+self.email+'\n'+str(self.permissions)

    class Meta:
        app_label = 'authentication'

class AuthBackend(object):
    def authenticate(self, email = None, password = None):
        user = object_manager.createUser(email = email)

        if user and user.password == password:
            return user

        return None

    def get_user(self, id):
        return object_manager.createUser(id = id)

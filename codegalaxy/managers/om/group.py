import dbw
import managers.om.user
import managers.om.objectmanager


import os.path


class Group:

    def __init__(self, id, group_name, group_type, created_on):
        '''
        @brief init of group
        @param id the if of the group
        @param group_name the name of the group
        @param group_type the type of the group
        @param created_on the date the group was created on
        '''
        self.id = int(id)
        self.group_name = group_name
        # private/public/...
        self.group_type = group_type
        self.created_on = created_on

    def getGroupPicture(self):
        group_picture = "group_pictures/{}.png".format(self.id)
        path = "./codegalaxy/static/" + group_picture

        if os.path.isfile(path):
            group_picture = group_picture
        else:
            group_picture = "media/group.png"
        return group_picture

    # list of users
    def allMembers(self):
        '''
        @return get all the members of a group, if there are none return empty list
        '''
        members_infos = dbw.getUsersInGroup(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        user_list = []
        for members_info in members_infos:
            user_list.append(object_manager.createUser(id=members_info['user_id']))
        return user_list

    def save(self):
        '''
        @brief save a group object
        '''
        dbw.updateGroup(self.id, self.group_name, self.group_type, self.created_on)

    def membershipPending(self, user_id):
        pending_group_memberships = dbw.getPendingGroupMemberships(user_id)

        for pending_group_membership in pending_group_memberships:
            if pending_group_membership['group_id'] == self.id:
                if pending_group_membership['user_id'] == user_id:
                    return True
        return False

    def insertMember(self, user_id, user_permissions, joined_on, status):
        '''
        @brief inserts a member in the group
        @param user_id the id of the user
        @param user_permissions the permissions of the user in this group
        @param joined_on the date the user joined on
        '''
        dbw.insertUserInGroup(self.id, user_id, user_permissions, joined_on, status)

    def deleteMember(self, user_id):
        dbw.deleteUserFromGroup(self.id, user_id)

    def getUserPermissions(self, user_id):
        if self.group_type == 0:
            return 0
        else:
            permissions = dbw.getGroupUserPermissions(self.id, user_id)
            return permissions[0]['user_permissions']

    def __str__(self):
        '''
        @brief string representation of the group
        '''
        return str(self.id) + ' ' + self.group_name + ' ' + str(self.group_type) + " " + str(self.created_on)

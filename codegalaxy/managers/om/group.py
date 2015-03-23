import dbw
import managers.om.user
import managers.om.objectmanager

class Group:

    def __init__(self, id, group_name, group_type, created_on):
        '''
        @brief init of group
        @param id the if of the group
        @param group_name the name of the group
        @param group_type the type of the group
        @param created_on the date the group was created on
        '''
        self.id = id
        self.group_name = group_name
        # private/public/...
        self.group_type = group_type
        self.created_on = created_on

    # list of users
    def allMembers(self):
        '''
        @return get all the members of a group, if there are none return empty list
        '''
        members_infos = dbw.getUsersInGroup(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        user_list = []
        for members_info in members_infos:
            user_list.append(object_manager.createUser(id = members_info['user_id']))
        return user_list


    def save(self):
        '''
        @brief save a group object
        '''
        dbw.updateGroup(self.id, self.group_name, self.group_type, self.created_on)

    def insertMember(self, user_id, user_permissions, joined_on, status):
        '''
        @brief inserts a member in the group
        @param user_id the id of the user
        @param user_permissions the permissions of the user in this group
        @param joined_on the date the user joined on
        '''
        dbw.insertUserInGroup(self.id, user_id, user_permissions, joined_on, status)

    def __str__(self):
        '''
        @brief string representation of the group
        '''
        return str(self.id) + ' ' + self.group_name + ' ' + str(self.group_type) + " " + str(self.created_on)

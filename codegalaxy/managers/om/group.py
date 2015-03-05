import dbw
import managers.om.user
import managers.om.objectmanager

class Group:
    def __init__(self,id,group_name,group_type):
        self.id = id
        self.group_name = group_name
        # private/public/...
        self.group_type = group_type

    # list of users
    def allMembers(self):
        members_infos = dbw.getUsersInGroup(self.id)
        object_manager = managers.om.objectmanager.ObjectManager()
        user_list = []
        for members_info in members_infos:
            user_list.append(object_manager.createUser(id = members_info['user_id']))
        return user_list


    def save(self):
        dbw.updateGroup(self.id,self.group_name,self.group_type)

    def insertMember(self, user_id, user_permissions):
        dbw.insertUserInGroup(self.id, user_id, user_permissions)

    def __str__(self):
         return str(self.id)+' '+self.group_name+' '+str(self.group_type)

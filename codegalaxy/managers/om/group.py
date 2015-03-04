import dbw
import managers.om.user

class Group:
    def __init__(self,id,group_name,group_type):
        self.id = id
        self.group_name = group_name
        # private/public/...
        self.group_type = group_type

    # list of users
    def allMembers(self):
        members_infos = dbw.getUsersInGroup(self.id)
        if members_infos:
            user_list = []
            for members_info in members_infos:
                user_id = members_info['user_id']
                user_info = dbw.getUserOnId(user_id)
                user_object = managers.om.user.User(user_id,user_info['first_name'],user_info['last_name'],
                user_info['is_active'],user_info['email'],user_info['permission'], user_info['password'])
                user_list.append(user_object)
            return user_list
        else:
            return None

    def save(self):
        dbw.updateGroup(self.id,self.group_name,self.group_type)

    def insertMember(self, user_id, user_permissions):
        dbw.insertUserInGroup(self.id, user_id, user_permissions)

    def __str__(self):
         return str(self.id)+' '+self.group_name+' '+str(self.group_type)

class Group:
    def __init__(self,id,group_name,group_type):
        self.id = id
        self.group_name = group_name
        # private/public/...
        self.group_type = group_type

    # list of users
    def allMembers(self):
        members_info = dbw.getUsersInGroup(self.id)
        if members_info:
            # We'll put the info in a regular list
            members_list = [ x['user_id'] for x in members_info]
            return members_list
        else:
            return None

    def __str__(self):
         return str(self.id)+' '+self.group_name+' '+str(self.group_type)

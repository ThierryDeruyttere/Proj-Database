import managers.om.user
import managers.om.objectmanager
import dbw
import datetime

import os.path


class Badge:

    def __init__(self, id, name, type, message, target_value, medal):
        self.id = id
        self.name = name
        self.type = type
        self.message = message
        self.target_value = target_value
        self.medal = medal

    def allUsersThatEarnedBadge(self):
        object_manager = managers.om.objectmanager.ObjectManager()

        finished_users = dbw.allBadgeEarnedUsers(self.id)

        user_objects = []

        for user in finished_users:
            user_objects.append(object_manager.createUser(id=user['user_id']))
        return user_objects

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self)
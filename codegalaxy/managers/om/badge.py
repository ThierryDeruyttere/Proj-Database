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

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self)
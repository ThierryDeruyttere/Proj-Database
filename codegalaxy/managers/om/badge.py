import managers.om.user
import managers.om.objectmanager
import dbw
import datetime

import os.path


class Badge:

    def __init__(self, id, name, type, message, target_value):
        self.id = id
        self.name = name
        self.type = type
        self.message = message
        self.target_value = target_value

    def __repr__(self):
        return str(self)

class hasBadge:
	def __init__(self, user_id, badge_id, current_value):
        self.user = id
        self.badge = name
        self.current_value = current_value

        self.finished = False

        if self.current_value >= self.badge.target_value:
        	self.finished = True

    def __repr__(self):
        return str(self)
import managers.om.user
import managers.om.objectmanager
import dbw
import datetime

import os.path

# Struct representing a Badge
class Badge:

    def __init__(self, id, name, type, message, target_value, medal):
        self.id = id
        self.name = name
        self.type = type
        self.message = message
        self.target_value = target_value
        self.medal = medal

    # Returns a string representing the path to the picture of a bronze/zilver or gold medal
    def getPicture(self):
        badge_picture = "media/icons/gold_badge.png"
        if self.medal == "gold":
            badge_picture = "media/icons/gold_badge.png"
        elif self.medal == "silver":
            badge_picture = "media/icons/silver_badge.png"
        elif self.medal == "bronze":
            badge_picture = "media/icons/bronze_badge.png"

        return badge_picture

    # Returns the dutch translation of the message
    def getDutchMessageTranslation(self):
        trans = dbw.getDutchMessageTranslation(self.id)
        dutch = trans['translation']
        return dutch

    # Returns the english original of the message
    def getEnglishMessage(self):
        trans = dbw.getEnglishMessage(self.id)
        english = trans['translation']
        return english

    # Returns User-objects of all the users that have earned this badge
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

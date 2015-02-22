import om.exerciselist
import om.exercise
import om.user
import om.group
import dbw
# Class that will build and work with the various objects representing the site
# will use SQL


class ObjectManager:
    '''Class which will consist of a few make-functions for objects by using SQL queries
    then some info-gathering functions for the views'''
    def __init__(self):
        pass

    # Uses the DB to create an object representing a user
    def createUser(self,id):
        user_info = dbw.getUserInformation(id)
        # SQL query voor user info
        user_object = om.user.User(id,user_info[0]["first_name"],user_info[0]["last_name"],
        user_info[0]["is_active"],user_info[0]["email"],user_info[0]["permission"])
        return user_object

    

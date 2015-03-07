
from managers.om import *

object_manager = objectmanager.ObjectManager()

# BASIC OVERLAP SCORE=====================================================================================

# returns the id's of all the lists the user with user_id made
def madeListIdsForUser(user_id):
    user = object_manager.createUser(user_id)
    made_lists = user.allPersonalLists()
    # All the id's of the made exercises
    return [made_list.exercises_list.id for made_list in made_lists]

# returns a list with all the items that occur in list2 but not list1
def differenceInLists(list1,list2):
    return [item for item in list2 if item not in list1]

# returns length of overlap by the amount of exercises the user made (*100)<-?
def checkOverlapScore(user_lists,other_lists):
    return (len([user_list for user_list in user_lists if user_list in other_lists])/len(user_lists))*100

# returns a list of tuples with:
#(list of items not made by user, overlap rating, other user's id)
def compareListWithOtherUsers(user_id):
    results = []
    made_list_ids = madeListIdsForUser(user_id)
    other_user_ids = object_manager.allUsers()
    for other_user_id in other_user_ids:
        other_made_list_ids = madeListIdsForUser(other_user_id)
        overlap_score = checkOverlapScore(made_list_ids,other_made_list_ids)
        result = (differenceInLists(made_list_ids,other_made_list_ids),overlap_score,other_user_id)
        results.append(result)
    return results

# MULTIPLIERS==============================================================================================

# friends are taken into account a bit more for the overlap_scores
def friendsMultiplier(user_id,other_user_id):
    user = object_manager.createUser(user_id)
    friends = user.allFriends()
    for friend in friends:
        if other_user_id = friend.id
            # NOTE: RANDOM VALUE
            return 1.2
    # not a friend -> no multiplier
    return 1

# MAIN FUNCTIONS===========================================================================================

def recommendListsForUser(user_id):
    comparison_tuples = compareListWithOtherUsers(user_id)
    # we split this result such that each list only occurs once, it gets


from managers.om import *

object_manager = objectmanager.ObjectManager()

# MULTIPLIERS==============================================================================================

# returns the amount of exerciselists a user has made with a certain subject
# if the dates parameter is true, older lists will count for less
# Subjects with a lower rating also count for less (no rating->count for half)
def scorePerSubjectForUser(user_id,dates,ratings):
    # map with key: subjectID and value:amount*multipliers
    subject_scores = {}
    # list of subjectIDs
    subject_ids=object_manager.getAllSubjectIDs()
    for subject_id in subject_ids:
        subject_scores[subject_id]=


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

    # returns a dictionary with key->list_id and value -> highest overlap score
    def splitListIds(user_id,comparison_tuples,friends):
        score_per_list_id = {}
        # for every tuple (comparison with other user)
        for comparison_tuple in comparison_tuples:
            # if we need to add the friends multiplier
            if friends:
                comparison_tuple[1] *= friendsMultiplier(user_id,comparison_tuple[2])
            # for every list_id in the difference
            for list_id in comparison_tuple[0]:
                # if the list is already in the dict
                if list_id in score_per_list_id:
                    # check if the score is lower than this one
                    if score_per_list_id[list_id]<comparison_tuple[1]:
                        # if so, chenge it
                        score_per_list_id[list_id]=comparison_tuple[1]
                # if it's not in the dict yet
                else:
                    # add it
                    score_per_list_id[list_id]=comparison_tuple[1]
        return score_per_list_id

# MAIN FUNCTIONS===========================================================================================

#parameters are the things held in account for the recommendations
# you can then either just list the ones with the highest score or random ones out of the top X highest
def recommendListsForUser(user_id,friends=True,dates=True,subjects=True,rating=True,highest=True):
    comparison_tuples = compareListWithOtherUsers(user_id)
    # we split this result such that each list only occurs once, it gets the highest
    # overlap_score out of all the tuples it is in
    score_per_list_id = splitListIds(user_id,comparison_tuples,friends)
    # now we can start adding the other multipliers

    # dates will give higher values to subjects/languages in recent exercises

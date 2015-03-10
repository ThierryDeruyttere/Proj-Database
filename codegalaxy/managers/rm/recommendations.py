
from managers.om import *
import datetime

object_manager = objectmanager.ObjectManager()

# SubjectMultiplierS==============================================================================================

#ARBITRAIR SubjectMultiplierSYSTEEM:
#avg vd Dates ouder dan week -> / 2
#Dates ouder dan maand -> / 4
#Recenter dan avg -> *1.2

def timeMultiplier(avg_date, avg_param_date):
    print('hm')
    param_multiplier = 1
    week = datetime.timedelta(days=7)
    month = datetime.timedelta(days=31)
    if avg_param_date >= month:
        SubjectMultiplier = 0.25
    elif avg_param_date >= week:
        SubjectMultiplier = 0.5
    if avg_param_date < avg_date:
        SubjectMultiplier *= 1.2
    return param_multiplier

def timeSubjectMultiplier(user, subject_id):
    avg_date_age = user.avgDateAge()
    avg_subject_date_age = user.avgSubjectDateAge(subject_id)
    return timeMultiplier(avg_date_age, avg_subject_date_age)

def timeProgrammingLanguageMultiplier(user, prog_lang_id):
    avg_date_age = user.avgDateAge()
    avg_prog_lang_date_age = user.avgProgrammingLanguageDateAge(prog_lang_id)
    return timeMultiplier(avg_date_age, avg_prog_lang_date_age)

#AVG Rating 5->100% | 4->80% | 3->60% | 2-> 40% | 1->20% (aka (20%*avg) maar dus minstens 20%)
#Deze % word afh van hoeveel de user gemiddeld rate +- een deel (5%?) gedaan

def ratingMultiplier(avg_rating, param_rating):
    param_score = param_rating * 0.2
    if param_rating > avg_rating:
        param_score += param_rating * 0.05
    else:
        param_score -= param_rating * 0.05
    return param_score

def ratingSubjectMultiplier(user, subject_id, default):
    avg_rating = user.averageRating(default)
    subject_rating = user.subjectRating(subject_id, default)
    return ratingMultiplier(avg_rating, subject_rating)

def ratingProgrammingLanguageMultiplier(user, subject_id, default):
    avg_rating = user.averageRating(default)
    prog_lang_rating = user.progLangRating(subject_id, default)
    return ratingMultiplier(avg_rating, prog_lang_rating)

# returns the amount of exerciselists a user has made with a certain subject
# if the dates parameter is true, older lists will count for less
# Subjects with a lower rating also count for less (no rating->count for half)
# default -> no rating will count for 50%, else wont be held into account
def scorePerSubjectForUser(user_id, dates, ratings, default):
    user = object_manager.createUser(id=user_id)
    # map with key: subjectID and value:amount*SubjectMultipliers
    subject_scores = {}
    # list of subjectIDs
    subject_ids = object_manager.allSubjectIDs()
    for subject_id in subject_ids:
        subject_scores[subject_id] = 1
        subject_scores[subject_id] = user.amountOfListsWithSubjectForUser(subject_id)
        # taking ratings of the subject into account
        subject_scores[subject_id] *= ratingSubjectMultiplier(user, subject_id, default)
        # taking into account how old the lists with that subject are
        subject_scores[subject_id] *= timeSubjectMultiplier(user, subject_id)
    return subject_scores

# returns the amount of exerciselists a user has made in a certain programming language
# if the dates parameter is true, older lists will count for less
# Subjects with a lower rating also count for less (no rating->count for half)
# default -> no rating will count for 50%, else wont be held into account
def scorePerProgrammingLanguageForUser(user_id, dates, ratings, default):
    user = object_manager.createUser(id=user_id)
    # map with key: subjectID and value:amount*SubjectMultipliers
    prog_lang_scores = {}
    # list of subjectIDs
    prog_lang_ids = object_manager.allProgrammingLanguageIDs()
    for prog_lang_id in prog_lang_ids:
        prog_lang_scores[prog_lang_id] = 1
        prog_lang_scores[prog_lang_id] = user.amountOfListsWithProgrammingLanguageForUser(prog_lang_id)
        # taking ratings of the subject into account
        prog_lang_scores[prog_lang_id] *= ratingProgrammingLanguageMultiplier(user, prog_lang_id, default)
        # taking into account how old the lists with that subject are
        prog_lang_scores[prog_lang_id] *= timeProgrammingLanguageMultiplier(user, prog_lang_id)
    return prog_lang_scores


# friends are taken into account a bit more for the overlap_scores
def friendsSubjectMultiplier(user_id, other_user_id):
    user = object_manager.createUser(id=user_id)
    friends = user.allFriends()
    for friend in friends:
        if other_user_id == friend.id:
            # NOTE: RANDOM VALUE
            return 1.2
    # not a friend -> no SubjectMultiplier
    return 1

# BASIC OVERLAP SCORE=====================================================================================

# returns the id's of all the lists the user with user_id made
def madeListIdsForUser(user_id):
    user = object_manager.createUser(id=user_id)
    made_lists = user.allPersonalLists()
    # All the id's of the made exercises
    return [made_list.exercises_list.id for made_list in made_lists]

# returns a list with all the items that occur in list2 but not list1
def differenceInLists(list1, list2):
    return [item for item in list2 if item not in list1]

# returns length of overlap by the amount of exercises the user made (*100)<-?
def checkOverlapScore(user_lists, other_lists):
    return (len([user_list for user_list in user_lists if user_list in other_lists]) / len(user_lists)) * 100

# returns a list of lists with:
#(list of items not made by user, overlap rating, other user's id)
def compareListWithOtherUsers(user_id):
    results = []
    made_list_ids = madeListIdsForUser(user_id)
    other_user_ids = object_manager.allUsers()
    for other_user_id in other_user_ids:
        # We don't want to compare the user to itself
        if other_user_id.id != user_id:
            other_made_list_ids = madeListIdsForUser(other_user_id.id)
            overlap_score = checkOverlapScore(made_list_ids, other_made_list_ids)
            result = [differenceInLists(made_list_ids, other_made_list_ids), overlap_score, other_user_id]
            results.append(result)
    return results

    # returns a dictionary with key->list_id and value -> highest overlap score
def splitListIds(user_id, comparison_tuples, friends):
    score_per_list_id = {}
    # for every tuple (comparison with other user)
    for comparison_tuple in comparison_tuples:
        # if we need to add the friends SubjectMultiplier
        if friends:
            comparison_tuple[1] *= friendsSubjectMultiplier(user_id, comparison_tuple[2])
        # for every list_id in the difference
        for list_id in comparison_tuple[0]:
            # if the list is already in the dict
            if list_id in score_per_list_id:
                # check if the score is lower than this one
                if score_per_list_id[list_id] < comparison_tuple[1]:
                    # if so, chenge it
                    score_per_list_id[list_id] = comparison_tuple[1]
            # if it's not in the dict yet
            else:
                # add it
                score_per_list_id[list_id] = comparison_tuple[1]
    return score_per_list_id

# MAIN FUNCTIONS===========================================================================================

def applyScoresToLists(score_per_list_id, scores, X_type):
    # How many subjects should we count per list? many high-ranked SJ -> better -> optellen?
    for list_id in score_per_list_id:
        ex_list = object_manager.createExerciseList(list_id)
        # 0 default? idk
        total_multiplier = 0
        amount_of_scores_counted = 0
        for score in scores:
            if ex_list.hasX(score, X_type):
                total_multiplier += scores[score]
                amount_of_scores_counted += 1
        score_per_list_id[list_id] *= (total_multiplier / amount_of_scores_counted)

def selectExercises(pool, highest, amount=10):
    if highest:
        sorted_pool = sorted(pool, key=lambda ex: ex[1])
        sorted_pool = sorted_pool[:amount]
        # we only need the exerciselist_ids
        return [ex[0] for ex in sorted_pool]
    # select random ones out of the pool
    else:
        pass

#parameters are the things held in account for the recommendations
# you can then either just list the ones with the highest score or random ones out of the top X highest
def recommendListsForUser(user_id, friends=True, dates=True, subjects=True, ratings=True, highest=True, default=False):
    comparison_tuples = compareListWithOtherUsers(user_id)
    # we split this result such that each list only occurs once, it gets the highest
    # overlap_score out of all the tuples it is in
    score_per_list_id = splitListIds(user_id, comparison_tuples, friends)
    # now we can start adding the other SubjectMultipliers
    subject_scores = scorePerSubjectForUser(user_id, dates, ratings, default)
    prog_lang_scores = scorePerProgrammingLanguageForUser(user_id, dates, ratings, default)
    print(score_per_list_id)
    print(subject_scores)
    print(prog_lang_scores)
    # dates will determine how long ago a user was interested in a subject(checking madelist)
    applyScoresToLists(score_per_list_id, subject_scores, 'Subject')
    print(score_per_list_id)
    applyScoresToLists(score_per_list_id, prog_lang_scores, 'Programming Language')
    print(score_per_list_id)
    #addDefault function to add basic exercises with low priority to recommend?

    recommended_exercises = selectExercises(score_per_list_id.items(), highest)
    return recommended_exercises

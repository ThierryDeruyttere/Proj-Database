import random
from managers.om import *
import datetime

object_manager = objectmanager.ObjectManager()

# default lists (chosen by us to recommend for new users)
default_lists = [1, 3, 8]
# Magic numbers=================================================================
# each factor (date/rating/...) has a certain importance/benchmark
# Time-based
recent = 10.0
older_than_month = 3.0
older_than_week = 5.0
older_than_average_date = 2.0  # Added to the two above
# Rating-based
percents_per_rating_star = 2.0  # 20% * rating (op 10)
difference_avg_rating = 0.5  # Added to above
# ETC
programming_language_importance = 3.0  # In comparison to subjects
default_list_entry = 20.0  # 20 is default vr recente
# Friends
friends_multiplier = 1.2  # (not friends -> this is 1)

# Recomendedlists (after we made one)
overlap_percentage = 0.4

# SubjectMultipliers==============================================================================================

# SubjectMultiplierSYSTEEM:

def timeMultiplier(avg_date, avg_param_date):
    param_multiplier = recent
    week = datetime.timedelta(days=7)
    month = datetime.timedelta(days=31)
    if avg_param_date >= week:
        param_multiplier = older_than_week
    if avg_param_date >= month:
        param_multiplier = older_than_month
    if avg_param_date < avg_date:
        param_multiplier -= older_than_average_date
    return param_multiplier

def timeSubjectMultiplier(user, subject_id):
    avg_date_age = user.avgDateAge()
    avg_subject_date_age = user.avgSubjectDateAge(subject_id)
    return timeMultiplier(avg_date_age, avg_subject_date_age)

def timeProgrammingLanguageMultiplier(user, prog_lang_id):
    avg_date_age = user.avgDateAge()
    avg_prog_lang_date_age = user.avgProgrammingLanguageDateAge(prog_lang_id)
    return timeMultiplier(avg_date_age, avg_prog_lang_date_age) * programming_language_importance

# AVG Rating 5->100% | 4->80% | 3->60% | 2-> 40% | 1->20% (aka (20%*avg) maar dus minstens 20%)
# Deze % word afh van hoeveel de user gemiddeld rate +- een deel (5%) gedaan

def ratingMultiplier(avg_rating, param_rating):
    param_score = param_rating * percents_per_rating_star  # 10 max
    if param_rating > avg_rating:
        param_score += difference_avg_rating
    else:
        param_score -= difference_avg_rating
    return param_score

def ratingSubjectMultiplier(user, subject_id, default):
    avg_rating = user.averageRating(default)
    subject_rating = user.subjectRating(subject_id, default)
    return ratingMultiplier(avg_rating, subject_rating)

def ratingProgrammingLanguageMultiplier(user, prog_lang_id, default):
    avg_rating = user.averageRating(default)
    prog_lang_rating = user.progLangRating(prog_lang_id, default)
    # Programming language is more important than subject
    return ratingMultiplier(avg_rating, prog_lang_rating) * programming_language_importance

# returns the amount of exerciselists a user has made with a certain subject
# if the dates parameter is true, older lists will count for less
# Subjects with a lower rating also count for less (no rating->count for half)
# default -> no rating will count for 50%, else wont be held into account
def scorePerSubjectForUser(user, dates, ratings, default):
    # map with key: subjectID and value:amount*SubjectMultipliers
    subject_scores = {}
    # list of subjectIDs
    subject_ids = object_manager.allSubjectIDs()
    for subject_id in subject_ids:
        subject_scores[subject_id] = 1
        subject_scores[subject_id] = user.amountOfListsWithSubjectForUser(subject_id)
        # taking ratings of the subject into account
        if ratings:
            subject_scores[subject_id] *= ratingSubjectMultiplier(user, subject_id, default)
        # taking into account how old the lists with that subject are
        if dates:
            subject_scores[subject_id] *= timeSubjectMultiplier(user, subject_id)
        if subject_scores[subject_id] < 1:
            subject_scores[subject_id] = 1
    return subject_scores

# returns the amount of exerciselists a user has made in a certain programming language
# if the dates parameter is true, older lists will count for less
# Subjects with a lower rating also count for less (no rating->count for half)
# default -> no rating will count for 50%, else wont be held into account
def scorePerProgrammingLanguageForUser(user, dates, ratings, default):
    # map with key: subjectID and value:amount*SubjectMultipliers
    prog_lang_scores = {}
    # list of subjectIDs
    prog_lang_ids = object_manager.allProgrammingLanguageIDs()
    for prog_lang_id in prog_lang_ids:
        prog_lang_scores[prog_lang_id] = 1
        prog_lang_scores[prog_lang_id] = user.amountOfListsWithProgrammingLanguageForUser(prog_lang_id)
        # taking ratings of the subject into account
        if ratings:
            prog_lang_scores[prog_lang_id] *= ratingProgrammingLanguageMultiplier(user, prog_lang_id, default)
        # taking into account how old the lists with that subject are
        if dates:
            prog_lang_scores[prog_lang_id] *= timeProgrammingLanguageMultiplier(user, prog_lang_id)
        if prog_lang_scores[prog_lang_id] < 1:
            prog_lang_scores[prog_lang_id] = 1
    return prog_lang_scores


# friends are taken into account a bit more for the overlap_scores
def friendsSubjectMultiplier(user, other_user_id):
    friends = user.allFriends()
    for friend in friends:
        if other_user_id == friend.id:
            # NOTE: RANDOM VALUE
            return friends_multiplier
    # not a friend -> no SubjectMultiplier
    return 1

# BASIC OVERLAP SCORE=====================================================================================

# returns the id's of all the lists the user with user_id made
def madeListIdsForUser(user):
    made_lists = user.allPersonalLists()
    # All the id's of the made exercises
    return [made_list.exercises_list.id for made_list in made_lists]

# returns a list with all the items that occur in list2 but not list1
def differenceInLists(list1, list2):
    return [item for item in list2 if item not in list1]

# returns length of overlap by the amount of exercises the user made (*100)<-?
def checkOverlapScore(user_lists, other_lists):
    if len(user_lists) == 0:
        return 0
    return (len([user_list for user_list in user_lists if user_list in other_lists]) / len(user_lists)) * 10

# returns a list of lists with:
#(list of items not made by user, overlap rating, other user's id)
def compareListWithOtherUsers(user):
    results = []
    made_list_ids = madeListIdsForUser(user)
    other_user_ids = object_manager.allUsers()
    for other_user_id in other_user_ids:
        # We don't want to compare the user to itself
        if other_user_id.id != user.id:
            other_made_list_ids = madeListIdsForUser(other_user_id)
            overlap_score = checkOverlapScore(made_list_ids, other_made_list_ids)
            result = [differenceInLists(made_list_ids, other_made_list_ids), overlap_score, other_user_id]
            results.append(result)
    return results

    # returns a dictionary with key->list_id and value -> highest overlap score
def splitListIds(user, comparison_tuples, friends):
    score_per_list_id = {}
    # for every tuple (comparison with other user)
    for comparison_tuple in comparison_tuples:
        # if we need to add the friends SubjectMultiplier
        if friends:
            comparison_tuple[1] *= friendsSubjectMultiplier(user, comparison_tuple[2])
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

# we default everything to one,so that in case of a small amount of data,
# lists are not kinda chosen randomly
def defaultScoreOne(score_per_list_id, dont_add):
    after_default = {}
    for i in range(object_manager.amountOfLists()):
        if i + 1 not in dont_add:
            if i + 1 in score_per_list_id:
                if score_per_list_id[i + 1] < 1:
                    after_default[i + 1] = 1
                else:
                    after_default[i + 1] = score_per_list_id[i + 1]
            else:
                after_default[i + 1] = 1
    return after_default

def addDefault(score_per_list_id, dont_add):
    for default_list in default_lists:
        if default_list not in dont_add:
            if default_list in score_per_list_id:
                if score_per_list_id[default_list] <= 10:
                    score_per_list_id[default_list] = default_list_entry
            else:
                score_per_list_id[default_list] = default_list_entry

def applyScoresToLists(score_per_list_id, scores, X_type):
    # How many subjects should we count per list? many high-ranked SJ -> better -> optellen?
    for list_id in score_per_list_id:
        ex_list = object_manager.createExerciseList(list_id, 1)
        # 0 default? idk
        total_multiplier = 0
        amount_of_scores_counted = 0
        for score in scores:
            if ex_list.hasX(score, X_type):
                total_multiplier += scores[score]
                amount_of_scores_counted += 1
        if amount_of_scores_counted != 0:
            score_per_list_id[list_id] *= (total_multiplier / amount_of_scores_counted)

def selectExercises(pool, highest, amount=10):
    if highest:
        sorted_pool = sorted(pool, key=lambda ex: ex[1], reverse=True)
        sorted_pool = sorted_pool[:amount]
        # we only need the exerciselist_ids
        return [ex[0] for ex in sorted_pool]
    # select random ones out of the pool
    else:
        # yet to implement
        pass

# parameters are the things held in account for the recommendations
# you can then either just list the ones with the highest score or random ones out of the top X highest
def recommendListsForUser(user, friends=True, dates=True, subjects=True, ratings=True, highest=True, default=False):
    # We compare which lists this user has made to the ones others have made
    # ([verchil in lijsten], overlap score, user obj)
    comparison_tuples = compareListWithOtherUsers(user)
    # We may not add these lists (made already)
    dont_add_obj_made = user.allPersonalLists()
    dont_add_obj_owned = user.ownedLists()
    dont_add = [obj.exercises_list.id for obj in dont_add_obj_made] + [obj.id for obj in dont_add_obj_owned]
    # we split this result such that each list only occurs once, it gets the highest
    # overlap_score out of all the tuples it is in
    score_per_list_id = splitListIds(user, comparison_tuples, friends)
    score_per_list_id = defaultScoreOne(score_per_list_id, dont_add)
    # now we can start adding the other SubjectMultipliers
    subject_scores = scorePerSubjectForUser(user, dates, ratings, default)
    prog_lang_scores = scorePerProgrammingLanguageForUser(user, dates, ratings, default)
    # dates will determine how long ago a user was interested in a subject(checking madelist)
    applyScoresToLists(score_per_list_id, subject_scores, 'Subject')
    applyScoresToLists(score_per_list_id, prog_lang_scores, 'Programming Language')
    # addDefault function to add basic exercises with low priority to recommend
    addDefault(score_per_list_id, dont_add)
    recommended_exercises = selectExercises(score_per_list_id.items(), highest)
    # returns a list with all the items that occur in list2 but not list1
    return recommended_exercises


# RECOMMEND NEXT EXERCISE====================================================================================================

# For this algorithm, we will only consider lists with the same language as
# the last one, many of the subjects will match and lastly, the difficulty
# will be dependant on the score the user got + the difficulty of the previous list

# score in %, difficulty in [1,2,3,4,5]
def decideDifficulty(difficulty, score):
    # >60% -> +1 diff
    # 40%-60% -> same diff
    # <40% -> -1 diff
    # nothing higher than 5/lower than 1
    if score >= 60 and difficulty < 5:
        return (difficulty, difficulty + 1)
    elif score <= 40 and difficulty > 1:
        return (difficulty - 1, difficulty)
    else:
        return (difficulty, difficulty)

# previous-> of the made list, new -> of a possible list
# ok, since we don't want to give too much advantage/disadvantage to long
# or short lists, depending on how many both lists have, a % overlap needed is calculated
def overlapNeeded(list):
    # we return a simple percentage
    return round(len(list) * overlap_percentage)

def subjectsMatch(previous, new):
    overlap_needed = overlapNeeded(new)
    overlap = [subject for subject in new if subject in previous]
    if overlap_needed <= len(overlap):
        return True
    else:
        return False


def madeIDs(user_obj):
    made_lists = user_obj.allPersonalLists()
    return [pers.exercises_list.id for pers in made_lists]

# parameter: personalExerciseListobject(or id?)
def recommendNextExerciseLists(previous_made_list, user, amount=4):
    new_exercise_lists = []
    # checking to make sure we dont try to suggest an already made list
    # we'll need the previously made lists
    made_ids = madeIDs(user)
    dont_add_obj_owned = user.ownedLists()
    dont_add_owned = [obj.id for obj in dont_add_obj_owned]
    new_difficulty = decideDifficulty(previous_made_list.exercises_list.difficulty, previous_made_list.score)
    prog_language = previous_made_list.exercises_list.programming_language.name
    subjects = previous_made_list.exercises_list.allSubjectIDs()
    possible_list_ids = object_manager.getExerciseListsOnProgLang(prog_language)
    for list_id in possible_list_ids:
        possible_list = object_manager.createExerciseList(list_id, 1)
        if possible_list.difficulty in new_difficulty:
            other_subjects = possible_list.allSubjectIDs()
            if subjectsMatch(subjects, other_subjects):
                if (list_id not in made_ids) and (list_id not in dont_add_owned):
                    new_exercise_lists.append(list_id)
    new_exercise_lists = new_exercise_lists[:amount]
    return new_exercise_lists

# EXERCISES LIKE THIS====================================================================================================================================
# Last of all, let's say we didnt just make an exercise but we just want a list that looks like this one

def listsLikeThisOne(list_id, user, amount=4):
    l_id = list_id
    new_exercise_lists = []
    # checking to make sure we dont try to suggest an already made list
    # we'll need the previously made lists
    made_ids = madeIDs(user)
    dont_add_obj_owned = user.ownedLists()
    dont_add_owned = [obj.id for obj in dont_add_obj_owned]
    list_obj = object_manager.createExerciseList(list_id, 1)
    # difficulties will be current +- 0/1
    prog_language = list_obj.programming_language.name
    subjects = list_obj.allSubjectIDs()
    possible_list_ids = object_manager.getExerciseListsOnProgLang(prog_language)
    for list_id in possible_list_ids:
        possible_list = object_manager.createExerciseList(list_id, 1)
        if possible_list.difficulty in [list_obj.difficulty - 1, list_obj.difficulty, list_obj.difficulty + 1]:
            other_subjects = possible_list.allSubjectIDs()
            if subjectsMatch(subjects, other_subjects):
                if (list_id not in made_ids) and (list_id not in dont_add_owned):
                    new_exercise_lists.append(list_id)

    if l_id in new_exercise_lists:
        new_exercise_lists.remove(l_id)
    # gives every element in the list an equal chance to appear
    random.shuffle(new_exercise_lists)
    # select the nessecary amount
    new_exercise_lists = new_exercise_lists[:amount]
    return new_exercise_lists

# I'm feeling Lucky!====================================================================================================================================
# Picks a random list the user hasn't made yet

def imFeelingLucky(current_user):
    if not current_user:
        return 0
    dont_add_obj = current_user.allPersonalLists()
    dont_add = [obj.exercises_list.id for obj in dont_add_obj]
    pool = [i for i in range(object_manager.amountOfLists()) if (i not in dont_add) and (i != 0)]
    if pool:
        return random.choice(pool)

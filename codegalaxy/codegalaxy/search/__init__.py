from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from managers.om import *
object_manager = objectmanager.ObjectManager()

def search(s_term='', s_users=False, s_groups=False, s_lists=False):
    # Get all user, group and list objects
    all_users = object_manager.allUsers()
    all_groups = object_manager.allPublicGroups()
    all_lists = object_manager.getAllExerciseLists()

    # Merge all user, group and list objects into one list
    all_search_obj = []
    if s_users:
        all_search_obj.extend(all_users)
    if s_groups:
        all_search_obj.extend(all_groups)
    if s_lists:
        all_search_obj.extend(all_lists)

    # Make a dict of the object with its seachString
    all_search = {obj: obj.searchString() for obj in all_search_obj}

    if s_term:
        # Fuzzy search
        results = process.extract(s_term, all_search, limit=10)

        # Search results have to have at least a 50% match
        filtered = [r[2] for r in reversed(sorted(results, key=lambda e: e[1])) if r[1] >= 50]

        return filtered

    else:
        return sorted(all_search, key=lambda e: e.group_name)

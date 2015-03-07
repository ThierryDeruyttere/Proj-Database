from django.http import HttpResponse
from django.shortcuts import render, redirect

from managers.om import *
import time

object_manager = objectmanager.ObjectManager()

def authenticate(email, password):
    '''
    @brief Check if the provided credentials are correct
    @param email The email to log in
    @param password the password to log in
    @return A user object if successful, None otherwise
    '''
    user = object_manager.createUser(email = email)

    if user and user.password == password:
        user.last_login = str(time.strftime("%Y-%m-%d"))
        user.save()
        return user
    return None

def require_login(*args):
    '''
    @brief A decorator to check for a logged in user, else redirect to a specified page
    '''
    def arg_wrapper(function = None):
        def f_wrapper(*args, **kwargs):
            user = None

            if 'current_user' in args[0].session:
                user = object_manager.createUser(id = args[0].session['current_user'])

            if user:
                return function(*args, **kwargs)
            else:
                return redirect(link)
        return f_wrapper

    if len(args) == 1 and callable(args[0]):
        link = "/login/"
        return arg_wrapper(args[0])
    else:
        link = args[0]

    return arg_wrapper

def logged_user(request):
    '''
    @brief Get the user that us currently logged in
    @param request The httpRequest object to be checked for a logged in user
    @return The user that is logged in or None
    '''
    user = None
    try:
        user = object_manager.createUser(id = request.session['current_user'])
    except:
        return None

    return user

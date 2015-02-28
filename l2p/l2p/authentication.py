from django.http import HttpResponse
from django.shortcuts import render, redirect

from om import *

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
        return user
    return None

def logged_in(function = None):
    '''
    @brief A 'is the user logged in' decorator, else redirect to a specified page
    '''
    def wrapper(*args, **kwargs):
        user = None

        if 'current_user' in args[0].session:
            user = object_manager.createUser(id = args[0].session['current_user'])

        if user:
            return function(*args, **kwargs)
        else:
            return redirect('/login')
    return wrapper

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

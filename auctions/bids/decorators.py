from django.http import HttpResponse
from django.shortcuts import redirect

def Unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('bids:index')
        response = view_func(request, *args, **kwargs)
        if not isinstance(response, HttpResponse):
            raise ValueError("The view did not return an HttpResponse object.")
        return response
    return wrapper_func

def Authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('bids:index')
        response = view_func(request, *args, **kwargs)
        if not isinstance(response, HttpResponse):
            raise ValueError("The view did not return an HttpResponse object.")
        return response
    return wrapper_func











"""
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your decorators here

def Unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('bids:index')

        return view_func(request, *args, **kwargs)

    return wrapper_func

def Authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('bids:index')

        return view_func(request, *args, **kwargs)

    return wrapper_func
"""
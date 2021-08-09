from django.http import HttpResponse
from django.shortcuts import redirect

#Decorator: It is a function that takes another function as a parameter
#           and lets us add some functionality before original function is called

#if user is logged-in than redirect to home, else return the function
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func








# eg:
# Here loginPage is passed as a parameter to unauthenticated_user as view_func and it is
# returned after running some tests(i.e wrapper function)
#
# @unauthenticated_user
# def loginPage(request):
#     ......

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

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name #get the name of 1st group

            #if that group is present in allowed_roles list then return a function else return a Httpsresponse
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator

#it is just a fix to coverup the fault caused by allowed_users decorator
#fault: if we use 'allowed_user' in home page then after customer login he will get
#       "You are not authorized to view this page" and cannot move anywhre else, so
#fix:   Redirect him to 'user' link if he is a customer
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name  # get the name of 1st group

        # if customer is accessing that page then redirect him to user page
        if group == 'customer':
            return redirect('user')
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func

# eg:
# Here we pass the list of allowed_roles to allowed_users function and then our decorator can access it
# @allowed_users(allowed_roles=["admin"])
# def home(request):
#     ........
#
# Here loginPage is passed as a parameter to unauthenticated_user as view_func and it is
# returned after running some tests(i.e wrapper function)
#
# @unauthenticated_user
# def loginPage(request):
#     ......

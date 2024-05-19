import json
from django.shortcuts import render
from django.http import HttpResponse

# ===================
# View: /secureweb/
# ===================
def home(request):
    return render(request, "secureweb/home.html")


# ============================
# View: /secureweb/playground
# ============================
def playground(request):
    return render(request, "secureweb/playground.html")


# ===================
# form login routes
# ===================
def login(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Extract the login type from the request parameters
        login_type = request.POST.get('login_type')
        
        _response = {'message' : 'incorrect'}

        # Handle the login form submission based on the login type
        if login_type == '1':
            # Handle login type 1
            # ...
            return HttpResponse('Login type 1 submitted')
        elif login_type == '2':
            # Handle login type 2
            # ...
            return HttpResponse('Login type 2 submitted')
        elif login_type == '3':
            # Handle login type 3
            # ...
            return HttpResponse('Login type 3 submitted')
        elif login_type == '4':
            # Handle login type 4
            # ...
            return HttpResponse('Login type 4 submitted')
        elif login_type == '5':
            # Handle login type 5
            # ...
            return HttpResponse('Login type 5 submitted')
        else:
            # Handle invalid login type
            # ...
            return HttpResponse('Invalid login type')

    # If the request method is not POST, render the login form
    return render(request, 'playground.html')


# todo: generate view for generate captchas

# ============================
# View: /secureweb/error
# ============================
def error(request):
    return render(request, "secureweb/error.html")



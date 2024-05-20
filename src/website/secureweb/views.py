from secureweb.models import Credentials
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# =============================
#  View: /secureweb/
# =============================
def home(request):
    return render(request, "secureweb/home.html")


# =============================
#  View: /secureweb/playground
# =============================
def playground(request):
    return render(request, "secureweb/playground.html")


# =============================
#  View: /secureweb/login 
# - form login routes
# =============================
@csrf_exempt
def login(request):
    if request.method != "POST":
        return render(request, "secureweb/error.html")
    
    # get login form ID
    login_form = request.POST.get('login_type')

    # extract login form values
    _email    = request.POST.get('username')
    _password = request.POST.get('password')

    # check if the email, password combination exists in the Credentials table
    message = ""
    try:
        credential = Credentials.objects.get(user_email=_email, user_password=_password)
        message = "correct"
        # send back correct message
    except Credentials.DoesNotExist:
        # email and password combination does not exist, display an error message
        message = "Invalid email or password"
    
    return JsonResponse({'message': message})
    
    
# ============================
#  View: /secureweb/error
# ============================
def error(request):
    return render(request, "secureweb/error.html")


# ============================
#  View: /secureweb/generate
# - generates new captchas
# ============================

# import authenticate module (authenticate.py)
# in this, we can create the validation functions for rate limiting, captchas, etc

# todo: fix home page (topic paragraph content alignment)

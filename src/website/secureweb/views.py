import random

from secureweb.scripts.Captchas import captchas

from secureweb.models import Credentials
from django.templatetags.static import static
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
    
    
# ===================================
#  View: /secureweb/captcha_generate 
# - generating new captcha images
# ===================================
def captcha_generate(request):
    # show a new captcha
    captcha = random.choice(captchas)
    captcha_url = static(f'images/captcha/{captcha}')
    
    print(f'captcha url: {captcha_url}')
    
    return JsonResponse({'captcha': captcha_url})
    
    
# ===================================
#  View: /secureweb/captcha_submit
# - form captcha submission 
# ===================================
@csrf_exempt
def captcha_submit(request):
    pass

    
# ============================
#  View: /secureweb/error
# ============================
def error(request):
    return render(request, "secureweb/error.html")




# import authenticate module (authenticate.py)
# in this, we can create the validation functions for rate limiting, captchas, etc
# todo: fix home page (topic paragraph content alignment)

import os
import random
import base64
import urllib.parse

import secureweb.scripts.Authenticate
from secureweb.scripts.Captchas import captchas

from secureweb.models import Credentials
from django.templatetags.static import static
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

# configure authenticator
_auth = secureweb.scripts.Authenticate.Auhentication()

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

    # extract login form values and form number
    _email    = request.POST.get('username')
    _password = request.POST.get('password')
    _form     = request.POST.get('login_type')

    # authenticate request
    _auth.process_request(request, [_email, _password], _form)
    _client = _auth.ip

    # -------------------------
    # handle blocked clients
    # -------------------------
    if _auth.ip in _auth.blacklisted_clients and _form == '2':
        message = f'You have been banned, all login attempts will be blocked'
        return JsonResponse({'message' : message})

    # -------------------------
    # handle lockedout clients
    # -------------------------
    if _email in _auth.locked_accounts and _form == '4':
        message = f'Your account is temporarily locked, contact the support team'    
        return JsonResponse({'message' : message})
    
    # -------------------------
    # handle normal clients
    # -------------------------
    
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
    return JsonResponse({'captcha': captcha_url})
    
    
# ===================================
#  View: /secureweb/captcha_submit
# - form captcha submission 
# ===================================
@csrf_exempt
def captcha_submit(request):
    if request.method != "POST":
        return render(request, "secureweb/error.html")
    
    # extract form values
    captcha_answer = request.POST.get('captcha_input')
    captcha_name   = request.POST.get('captcha_name')
    
    # remove the file extension
    name, file_extension = os.path.splitext(captcha_name)
    name = urllib.parse.unquote(name)
    
    # check captcha
    answer = False
    decoded_bytes = base64.b64decode(name)
    decoded_string = decoded_bytes.decode('utf-8')
    
    if captcha_answer == decoded_string:
        answer = True
    
    # return result
    new_captcha = random.choice(captchas)
    result = {
        'message' : 'correct' if answer else 'Incorrect, try again', 
        'captcha' : new_captcha
    }
    
    return JsonResponse(result)

    
# ============================
#  View: /secureweb/error
# ============================
def error(request):
    return render(request, "secureweb/error.html")

'''
    TODO:
    1. [x] fix home page (topic paragraph content alignment)
    2. [x] complete Authenticate.py for login form security
        - [x] request logging
        - [?] rate limiting 
        - [?] account lockout times
        - [?] blacklisting
        - [x] differentiate security measures for each login form
    3. [x] update utilties scripts with new routes & to work on windows
    4. [x] Add function header comments
    5. [ ] update README.md
        - info on each script (monitor, proxies, attack)
        - add gif demo of unsuccesful attempts for each login
        - add gif demo of attack script
        - add requirements.txt (dependencies)
    6. [ ] Clean up old code (remove)
    7. [ ] Rename project
'''

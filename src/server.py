
# imports
import os
import random
import base64
import logging
import urllib.parse
from markupsafe import escape
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, url_for, redirect, make_response


# make flask instance
app = Flask(__name__)  

# setup login form credentials
passwords = [line.strip() for line in open('utils/scripts/passwords', 'r')]
credentials = {
    1: ('admin@secure.com', random.choice(passwords)),
    2: ('admin@secure.com', random.choice(passwords)),
    3: ('admin@secure.com', random.choice(passwords)),
    4: ('admin@secure.com', random.choice(passwords)),
    5: ('admin@secure.com', random.choice(passwords))
}

# setup captcha files
captcha_solved = False
captcha_directory = 'static/images/captcha'
captchas = [filename for filename in os.listdir(captcha_directory)]

'''
    =======================================
            Configure server logging
    =======================================
'''

# setups up terminal and file logging
def loggging():
    # logs to terminal
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console_handler.setFormatter(formatter)
    console_handler.addFilter(log_filter)
    root_logger.addHandler(console_handler)

    # logs to a file
    login_logger = logging.getLogger('login')
    login_handler = logging.FileHandler('login.log') 
    login_handler.setLevel(logging.INFO)
    login_formatter = logging.Formatter('%(asctime)s - %(message)s')
    login_handler.setFormatter(login_formatter)
    login_logger.addHandler(login_handler)


# filter out login-logs from terminal logger
def log_filter(record):
    string_to_exclude = "Username" 
    return string_to_exclude not in record.getMessage()

'''
    =======================================
            Handle 'GET' routes 
    =======================================
'''

# home page
@app.route('/')
def home():
    return render_template('home.html')


# learn page
@app.route('/learn')
def learn():
    return render_template('learn.html')


# demo page
@app.route('/demo')
def demo():
    return render_template('demo.html')


# 403 error page
@app.route('/error')
def error():
    return render_template('403.html')

'''
    =======================================
            Handle login submissions
    =======================================
'''

# validate login credentials
def validate(username, password, form_number):
    
    response_data = {'message': 'incorrect'}

    # look up credentials
    if form_number in credentials:
        expected_username, expected_password = credentials[form_number]
        if username == expected_username and password == expected_password:
            response_data = {'message': 'correct'}

    return response_data


# handle rating limiting
def rate_limit(ip):
    logs = 'login.log'
    
    # define the allowed attempts per minute
    rate_limit_threshold = 5
    rate_limit_window = 60

    # calculate the time threshold (1 minute ago)
    time_threshold = datetime.now() - timedelta(seconds=rate_limit_window)

    # read the log file and count the login attempts for the same IP address within the time window
    attempts = 0
    with open(logs, 'r') as log_file:
        for line in log_file:
            if 'IP: ' + ip in line:
                timestamp_str = line.split(' - ')[0]
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                if timestamp > time_threshold:
                    attempts += 1

    # check if attempts exceeds threshold
    if attempts >= rate_limit_threshold:
        print(f'Rate limit exceeded for client {ip}. Denied access.')
        return 'rate limited'
    
    return 'True'


# handle login security
def security(ip, form_number):
    # handle security for each login form
    global captcha_solved

    # [no security]
    if form_number == 1:
        pass    

    # [rate limiting]
    if form_number == 2:
        return rate_limit(ip)
     
    # [captcha]  
    if form_number == 3:
        # check captcha
        if captcha_solved:
            captcha_solved = False
        else:
            return 'invalid captcha'
        
    return 'True'


# handle login submission
@app.route('/login_<int:form_number>', methods=['POST'])
def login(form_number):
    # get form data
    username = request.form['username']
    password = request.form['password']

    # get client's IP address
    client_address = request.remote_addr
    
    # handle login security
    grant_acess = security(client_address, form_number)
    
    # unauthorized access
    if grant_acess == 'rate limited':
        return jsonify({'message': 'Try again later, account has reached the maximum number of login attempts'})

    # invalid captcha
    if grant_acess == 'invalid captcha':
        return jsonify({'message': 'Captcha error'})

    # suspcious activity
    if grant_acess == 'account lockout':
        return jsonify({
            'message' : grant_acess, 
            "redirect_url": "/error"
        })
        
        
    # log request
    login_logger = logging.getLogger('login')
    login_logger.info(
        f"IP: {client_address}, Username: {username}, Password: {password}"
    )

    # return login validation result
    response_data = validate(username, password, form_number)
    return jsonify(response_data)

'''
    =======================================
            Handle captcha submissions
    =======================================
'''

# handle generating captchas
@app.route('/generate')
def generate_captcha():
    # create new captcha
    captcha = random.choice(captchas)    
    result = {
        'captcha' : url_for('static', filename=f'images/captcha/{captcha}')
    }
    return jsonify(result) 


# checks if the captcha is valid
def check_captcha(value, file):
    global captcha_solved
    
    # Remove the file extension
    name, file_extension = os.path.splitext(file)
    name = urllib.parse.unquote(name)
    
    # check captcha
    answer = False
    decoded_bytes = base64.b64decode(name)
    decoded_string = decoded_bytes.decode('utf-8')
    
    if value == decoded_string:
        answer = True
        captcha_solved = True
    
    # return result
    new_captcha = random.choice(captchas)
    result = {
        'message' : 'correct' if answer else 'Incorrect, try again',
        'captcha' : new_captcha
    }
    return jsonify(result) 


# handle captcha submissions
@app.route('/captcha_submit', methods=['POST'])
def captcha():
    # get captcha input
    value = request.form['captcha_input']
    file = request.form['captcha_name']
    return check_captcha(value, file)



# start
if __name__ == '__main__':
    # setup logging & start server
    loggging()
    app.run()
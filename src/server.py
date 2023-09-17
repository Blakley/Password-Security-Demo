

# imports
import random
import logging
from markupsafe import escape
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, redirect, make_response


# make flask instance
app = Flask(__name__)  

# setup login form credentials
passwords = [line.strip() for line in open('utils/passwords', 'r')]
credentials = {
    1: ('reece@secure.com',   random.choice(passwords)),
    2: ('sarah@secure.com',   random.choice(passwords)),
    3: ('anthony@secure.com', random.choice(passwords)),
    4: ('admin@secure.com',   random.choice(passwords)),
    5: ('brute@secure.com',   random.choice(passwords))
}

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


# handle login security
def security(ip, form_number):
    # handle security for each login form

    # [no security]
    if form_number == 1:
        pass    

    # [rate limiting]
    if form_number == 2:
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


# handle login submission
@app.route('/login_<int:form_number>', methods=['POST'])
def login(form_number):
    # get form data
    username = request.form['username']
    password = request.form['password']

    # get client's IP address
    client_address = request.remote_addr
    
    # log request
    login_logger = logging.getLogger('login')
    login_logger.info(
        f"IP: {client_address}, Username: {username}, Password: {password}"
    )

    # handle login security
    grant_acess = security(client_address, form_number)
    
    # unauthorized access
    if grant_acess == 'rate limited':
        # return jsonify({"redirect_url": "/error"}) [will be used for ip blocking @login form4]
        response = make_response('', 401)
        return response
        
    # return login validation result
    response_data = validate(username, password, form_number)
    return jsonify(response_data)



# start
if __name__ == '__main__':
    # setup logging & start server
    loggging()
    app.run()
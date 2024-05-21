# =========================================
# Configuration for login form(s) security
# =========================================

from collections import Counter
from datetime import datetime, timedelta

'''
'''
class Auhentication:
    def __init__(self):
        self.configure()


    # ----------------------------------------
    #
    # ----------------------------------------
    def configure(self):
        # lockedout clients that have exceeded threshold
        self.locked_accounts = []
        # blacklisted clients that have exceeded threshold
        self.blacklisted_clients = []
        
        # allowed login attempts for login form 2 (rate_requests) and login form 4 (rate_lockout)
        self.rate_requests  = 5
        self.rate_lockout   = 3
        
        
    # ----------------------------------------
    # 
    # ----------------------------------------
    def process_request(self, request, credentials, _form):
        self.request = request 
        self.credentials = credentials
        self._form = _form
        
        '''
            login form 1: no security
            login form 2: rate limiting
            login form 3: captcha
            login form 4: lockout policy
        '''
        
        # get requesting client & update the log file
        self.identifiy_request()
        
        # check client request rate
        acceptable = True
        if self._form == '2' or self._form == '4':
            acceptable = self.ratelimit_request()
        
        # log request
        if acceptable:
            self.log_request()

        
    # ----------------------------------------
    #
    # ----------------------------------------
    def identifiy_request(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        
        self.ip = None

        if x_forwarded_for:
            self.ip = x_forwarded_for.split(',')[0]
        else:
            self.ip = self.request.META.get('REMOTE_ADDR')


    # ----------------------------------------
    #
    # ----------------------------------------
    def ratelimit_request(self):
        # skip requests that are blacklisted
        if self.ip in self.blacklisted_clients and self._form == '2':
            return False
        
        # define the allowed attempts per minute
        attempts_per_minute = 60

        # calculate the time threshold (1 minute ago)
        previous_time = datetime.now() - timedelta(seconds = attempts_per_minute)

        # calculate login attempts (for either form) within 1 minute for the client
        attempts_form_2 = 1
        attempts_form_4 = 1
        
        last_timestamp = ""
        
        with open('utilities/login.log', 'r') as log_file:
            for line in log_file:
                timestamp_str   = line.split(',')[0] 
                timestamp       = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                last_timestamp  = timestamp
                
                login_form_number = (line.split(',')[4]).strip()
                login_form_number = login_form_number.replace('Login Form: ', '')
                
                if timestamp >= previous_time:
                    # increment requests for rate limit
                    if login_form_number == '2':
                        attempts_form_2 += 1
                        
                    # increment requests for lockout    
                    if login_form_number == '4':
                        attempts_form_4 += 1 
                    
        # check if attempts exceeds threshold, blacklist client if so
        if attempts_form_2 >= self.rate_requests and self._form == '2':
            self.blacklist_request()
            return False
            
        # check if attempts exceeds threshold, lockout account if so
        if attempts_form_4 >= self.rate_lockout and self._form == '4':
            self.lockout_request()
            return False
            
        return True
    
    
    # ----------------------------------------
    #
    # ----------------------------------------
    def lockout_request(self):
        self.locked_accounts.append(self.credentials[0])


    # ----------------------------------------
    #
    # ----------------------------------------
    def blacklist_request(self):
        self.blacklisted_clients.append(self.ip)


    # ----------------------------------------
    #
    # ----------------------------------------
    def log_request(self):
        _time = datetime.now()
        _log  = f'{_time}, {self.ip}, Username: {self.credentials[0]}, Password: {self.credentials[1]}, Login Form: {self._form}\n' 
        
        with open('utilities/login.log', 'a+') as log_file:
            log_file.write(_log)


# authentication instance
_auth = Auhentication()
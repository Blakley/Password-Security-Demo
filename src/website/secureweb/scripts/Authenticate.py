# =========================================
# Configuration for login form(s) security
# =========================================

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
        #
        self.locked_accounts = []
        #
        self.locked_account_attempts = {} 
        #
        self.locked_account_threshold = 5
        #
        self.black_listed_ips = []
        
        
    # ----------------------------------------
    #
    # ----------------------------------------
    def process_request(self, request, resource, credentials=None):
        self.request = request 
        self.credentials = credentials
        
        # get requesting client & update the log file
        self.identifiy_request()
        
        if resource == 'login':
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
    def log_request(self):
        _time = datetime.now()
        _log  = f'{_time}, {self.ip}, Username: {self.credentials[0]}, Password: {self.credentials[1]}\n' 
        
        with open('utilities/login.log', 'a+') as log_file:
            log_file.write(_log)
    


# authentication instance
_auth = Auhentication()
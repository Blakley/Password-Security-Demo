# =========================================
# Configuration for login form(s) security
# =========================================

import logging
from datetime import datetime, timedelta

# 
locked_accounts = []
locked_account_attempts = {} 
locked_account_threshold = 5

#
black_listed_ips = []



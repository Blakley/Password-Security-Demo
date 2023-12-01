# Project notes

### /home
Homepage for the website

### /login
Page containing demo login forms to showcase potential brute forcing techniques / mitigations. 

- Login Form 1: No security
- Login Form 2: IP Rate Limiting
- Login Form 3: Captcha
- Login Form 4: Account lockout & IP blocking

### /learn
Page detailing Rate limiting, Captchas, Account lockout, IP blacklisting, and MFA. 
Namely, what they are, how they’re implemented, and pros of cons of each.

# Web server and Scripts

### server.py
Sets up a webserver and handles get/posts requests made and the security of the website on the server.

### monitor.py
Constantly monitors the client log file, used in demonstration.

### login.log
Displays the Data/Time, IP Address, and attempted credentials on the login forms.

### attack.py
Script demonstrating how attackers bruteforce credentials on the login demo forms.

### proxies.py
This script creates private ip addresses on the computer which act like
proxies to allow bypassing rate limit & IP blocking bruteforcing.
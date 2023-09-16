# Password Bruteforcing Demo

An educational project showcasing brute forcing techniques and common mitigations. 

## Screenshots

## Dependenices

Have Python3 installed and use pip to install the following:
```
    pip install Flask
    pip install termcolor
```

## Understanding the scripts

Provided below is a general overview of each script file.

### attack.py

`attack.py` is a password bruteforcing script that attempts to figure out the login credentials for each login form.

### monitor.py

`monitor.py` is a script file that will continually monitor updates to the `login.log` file, which shows the login attempts to each login form.
This script is a useful script that provides a visual of how to monitor webserver logs

### proxies.py

`proxies.py` is script that creates numerous [loopback interfaces](https://techhub.hpe.com/eginfolib/networking/docs/switches/common/15-18/5998-8158_bog/content/ch06s03.html#:~:text=A%20loopback%20interface%20is%20a,other%20switch%20interface%20is%20up.) that's used to mimic a proxy pool used to bypass
rate limiting and ip blocking.

## Deployment

* To start the server, execute the `server.py` file
* You can test bruteforcing either login form by either using a tool like [Burp Suite](https://portswigger.net/burp), [John the Ripper](https://github.com/openwall/john), or by running the `attack.py` file as explained by.

### Todo
* Test security for Login Form 2
* Implement security for Login Forms 3, 4, 5, and 6
* Replace dummy text with researched text/topics
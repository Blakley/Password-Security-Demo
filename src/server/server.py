# imports
import os
import time
import logging
import webbrowser
import http.server
import socketserver
from termcolor import colored
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs


# login credentials
credentials = {
	'1': ('reece',   'abracadabra'),		# page 1
	'2': ('sarah',   'chickenwing101'),		# page 2
	'3': ('anthony', 'ezmoney'),			# page 3
	'4': ('admin',   'WSBadmin'),			# page 4
	'5': ('brute',   'letmein4')			# page 5
}


'''
	Webserver class:
		Setups a local webserver at localhost:8000
		to handles get and posts requests
'''
class Server(http.server.BaseHTTPRequestHandler):
	
	# handle server get requests
	def do_GET(self):

		# folder directory
		directory = os.path.dirname(os.path.realpath(__file__))

		# handle css files
		if 'css' in self.path:
			directory = '/' + directory.replace('server', 'css')

		# handle html pages
		if 'html' in self.path:
			directory = '/' + directory.replace('server', 'html')

		# set page path
		self.path = os.path.join(directory, self.path[1:])

		# open requested page
		try:
			with open(self.path[1:], 'rb') as file:
				content = file.read()
				self.open_route(content, 'get')

		except Exception as e:
			self.invalid_route()


	# handle server post requests
	def do_POST(self):

		# retrieve post contents
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length).decode('utf-8')
		parsed_data = parse_qs(post_data)

		# get login form data
		username = parsed_data.get('username', [''])[0]
		password = parsed_data.get('password', [''])[0]
		client_address = self.client_address[0]

		# log request
		logging.info(
			f"IP: {client_address}, Username: {username}, Password: {password}, Page: {self.path}"
		)

		# implement login page security		
		grant_access = self.security(self.path, client_address)
		if not grant_access:
			self.failed_login('Rate limit exceeded')
			return

		# invalid post request
		if 'login' not in self.path:
			self.invalid_route()
			return

		# === handle each login route ===
		
		i = 1
		r = ['1', '2', '3', '4', '5']

		# [test] : all login routes
		if any(f'login_{num}' in self.path for num in r):
			# get login page index
			i = int(self.path.split('_')[-1])

			if self.validate(username, password, i):

				# open route
				if i <= 4:
					self.open_route(f'login_{i + 1}.html', 'post')
				else:
					self.open_route('end.html', 'post')
				return


		# handle failed login : don't update page
		self.failed_login('')


	# security for given login page
	def security(self, page, address):

		# security for login page 1 : [no security]
		if '1' in page:
			pass
		

		# security for login page 2 : [rate limit]
		if '2' in page:

			# get log file path
			logs = 'logs/clients.log'
			
			# define the allowed attempts per minute
			rate_limit_threshold = 5
			rate_limit_window = 60

			# calculate the time threshold (1 minute ago)
			time_threshold = datetime.now() - timedelta(seconds=rate_limit_window)

			# read the log file and count the login attempts for the same IP address within the time window
			attempts = 0
			with open(logs, 'r') as log_file:
				for line in log_file:
					if 'IP: ' + address in line:
						timestamp_str = line.split(' - ')[0]
						timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
						if timestamp > time_threshold:
							attempts += 1

			# check if attempts exceeds threshold
			if attempts >= rate_limit_threshold:
				print(f'Rate limit exceeded for {address}. Denied access.')
				return False


		return True


	# validate user login
	def validate(self, username, password, page_index):
		# check if username, password combination matches required
		if str(page_index) in credentials:
			d_user, d_pass = credentials[str(page_index)]
			if username == d_user and password == d_pass:
				return True

		return False


	# handle failed login attempt
	def failed_login(self, message):
		self.send_response(204) 
		
		# set login error cookie
		if len(message) > 1:
			expiration_time = datetime.now() + timedelta(minutes=1)
			expiration_str = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
			self.send_header('Set-Cookie', f'login_error={message}; Path=/; Expires={expiration_str}')
		
		self.end_headers()


	# handle processing request 
	def open_route(self, content, method):

		# handle get request
		if method == 'get':
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(content)
		else:
			# handle post request
			self.send_response(302)
			self.send_header('Location', content)
			self.end_headers()


	# handle invalid page request
	def invalid_route(self):

		self.send_response(500) 
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write('500 - Internal Server Error'.encode('utf-8'))



# start script
if __name__ == '__main__':
	# set server port
	port = 8000
	host = 'localhost' 

	# configure webserver logs
	logging.basicConfig(filename='logs/clients.log', level=logging.INFO, format='%(asctime)s - %(message)s')

	# run server
	with socketserver.TCPServer((host, port), Server) as web:

		c = colored('WebServer', 'cyan', attrs = ['bold', 'underline'])
		p = colored(f'{port}', 'magenta', attrs = ['reverse'])
		print(f"\n{c} running on port: {p}\n")

		# open server home page
		webbrowser.open(f'http://{host}:8000/home.html')

		try:
			web.serve_forever()
		except KeyboardInterrupt:
			pass

		web.server_close()




'''
                    TODO 
    ===================================

	1. Refactor code to make more readable
	2. Make one /login.html page instead of multiple. this page will contain multiple login forms
    3. Think of and implement website theme (bank, social media platform, streamingsite, etc)
	
'''
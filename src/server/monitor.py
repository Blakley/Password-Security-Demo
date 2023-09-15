# imports
import os
import time
import platform


'''
    Monitors the clients.log file for changes
    the file is updated whenever a login forum is submitted
'''
class Monitor(object):
    def __init__(self):
        self.output_log = 'logs/clients.log'
        self.monitor()

    # capture new traffic
    def monitor(self):
        previous_time = 0

        while True:
            current_time = os.path.getmtime(self.output_log)
            
            if current_time != previous_time:
                # clear the terminal screen based on the platform
                if platform.system() == 'Windows':
                    os.system('cls') 
                else:
                    os.system('clear')
                
                # print file content
                with open(self.output_log, 'r') as file:
                    content = file.read()
                    print(content)

                # Update the previous time
                previous_time = current_time

            time.sleep(1)


# start
if __name__ == '__main__':
    m = Monitor()
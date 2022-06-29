import os
import time

while 1:
    os.system('python new_package_to_queue.py')
    os.system('python update_package_to_queue.py')
    time.sleep(60)

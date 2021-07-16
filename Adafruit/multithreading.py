
# https://www.geeksforgeeks.org/multithreading-python-set-1/

# A thread is an entity within a process
# that can be scheduled for execution.

# Also, it is the smallest unit of processing
# that can be performed in an OS (Operating System).

# In simple words, a thread is a sequence of such instructions
# within a program that can be executed independently of other code.

# For simplicity, you can assume that a thread is simply a subset of a process!

# ==================================================

# Python program to illustrate the concept
# of threading
# importing the threading module

import threading
import livemqtt as lm
import time

with open('data.txt', 'w') as f:
    f.write('payload')

def savedata():
    while(True):
        time.sleep(5)

        with open('data.txt', 'r') as f:
            onoff = f.read()
        print(onoff)

if __name__ == "__main__":
	# creating thread
	t1 = threading.Thread(target=lm.threadone)
	t2 = threading.Thread(target=savedata)

	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()

	# wait until thread 1 is completely executed
	t1.join()
	# wait until thread 2 is completely executed
	t2.join()

	# both threads completely executed
	print("Done!")

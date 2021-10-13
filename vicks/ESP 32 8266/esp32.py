# https://www.c-sharpcorner.com/article/firebase-crud-operations-using-python/

# https://console.firebase.google.com/u/0/project/led-blink-wifi/database/led-blink-wifi-default-rtdb/data

# ==============================================

from vicksbase import firebase as vix

firebase_obj = vix.FirebaseApplication('https://led-blink-wifi-default-rtdb.firebaseio.com/', None)

def pull():
    result = firebase_obj.get('led1', None)
    print('\n   Value fetched = ', result, end='\n\n')

def push(data):
    firebase_obj.put('/','led1', data)
    print('\nUpdated...\n')


# Running in CMD like...
#
# C:\Users\Vicky\Desktop\Repository\firebase\esp32_led>python
# Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 16:30:00) [MSC v.1900 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>>
# >>> import esp32 as v
# >>>
# >>> v.pull()
#
#    Value fetched =  0
#
# >>> v.push(1)
#
# Updated...
#
# >>> v.pull()
#
#    Value fetched =  1
#
# >>> v.push(0)
#
# Updated...
#
# >>> v.pull()
#
#    Value fetched =  0
#
# >>>


# if __name__ == '__main__':
#
#     val = int(input('\n Enter (1/0) : '))
#     push(val)
#
#     pull()
#     input('\n   Click Enter to Exit...')

# =================================================

# from firebase import firebase
# fb_app = firebase.FirebaseApplication('https://led-blink-wifi-default-rtdb.firebaseio.com/', None)
# result = fb_app.get('/led1', None)
# input(result)

# Output...

# C:\Users\Vicky\Desktop\Repository\firebase\Firebase-CRUD>python esp32.py
# Traceback (most recent call last):
#   File "esp32.py", line 25, in <module>
#     from firebase import firebase
# ImportError: cannot import name 'firebase' from 'firebase' (unknown location)

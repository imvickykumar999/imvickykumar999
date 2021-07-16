from gtts import gTTS

content = '''
A video of Mika Singh has surfaced online, in which he can be seen visiting Kamaal R Khan's house and claiming that the latter sold the property out of fear. "Please don't sell all your other houses because I have no personal enmity with you," he said. "Don't be scared. I won't beat you up," Mika added.
'''

tts = gTTS(content)
tts.save('hello.mp3')

import os
os.system('hello.mp3')

# =================================================

# import pyttsx3
# engine = pyttsx3.init()
#
# # rate = engine.getProperty('rate')   # getting details of current speaking rate
# # print (rate)                        #printing current voice rate
# # engine.setProperty('rate', 150)     # setting up new voice rate
#
# # volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# # print (volume)                          #printing current volume level
# # engine.setProperty('volume',1.0)
#
# voices = engine.getProperty('voices')       #getting details of current voice
# # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)
#
# engine.say(content)
# engine.runAndWait()

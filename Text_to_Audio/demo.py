import os

from gtts import gTTS

# text = 'Welcome buddy, this is my first audio script, cheers'
text = open('demo.txt', 'r').read()
language = 'en'
output = gTTS(text=text, lang=language, slow=True)
output.save('fileoutput.mp3')
os.system('start fileoutput.mp3')

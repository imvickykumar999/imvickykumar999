from ShazamAPI import Shazam

mp3_file_content_to_recognize = open('Stebin Ben - Baarish Ban Jaana_192(PagalWorld.com.se).mp3', 'rb').read()

shazam = Shazam(mp3_file_content_to_recognize)
recognize_generator = shazam.recognizeSong()
while True:
    print(next(recognize_generator)) # current offset & shazam response to recognize requests


import pandas as pd
# df = pd.read_csv ('Event Registration (Responses) - Form Responses 1.csv')
# df = df.drop(df.index[7])

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "imvickykumar999@gmail.com"
# toaddr = list(set(df['EMAIL ID ( Team Leader )']))

toaddr = [
          'ashish99anonymous@gmail.com',
          'Sanjusharma14021999@gmail.com',
          '19ERECS055.rajdeep@rietjaipur.ac.in',
          'omjeeyadav563@gmail.com',
          'imvickykumar999@gmail.com',
         ]

print(toaddr)

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ','.join(toaddr)

msg['Subject'] = ">>> Hackathon PPT Missing !!!"
body = f'''
Hi,
We hope that this email finds you in the best of health.

Please note that the deadline for the idea submission for the Hackathon- “HackRIETJ”, is 21 June 2021 11:59 PM IST.

We encourage early submissions so that you do not face any last minute hassles.

No late submissions will be acknowledged and responsibility of making the submission before the due time lies solely with the participants.

Participants must keep in mind the following instructions in regards to the idea submission:

You can change your submissions by clicking on ‘Submission’ and then ‘Edit Submission’, anytime before the submission deadline.

Please make all your submissions well before the submission deadline to avoid any last-minute problems.

>>> Kindly Submit your PPT in the given form...
(Rename as TeamName_YourName.pptx) :
https://docs.google.com/forms/d/e/1FAIpQLSfZGtewUdn8APM3j7J4D3HLGjtV0f2cMjaBIuP9AegSTNUKww/viewform

>>> Kindly use the PPT Template from this link : https://drive.google.com/file/d/10f-9wGzc3rIK7vI02owY9WKVzDjaRovi/view?usp=sharing

Join our WhatsApp Group for updates and queries: https://chat.whatsapp.com/Jy2ZdTbfmQoEFtQjNubMpO

We wish you good luck! Keep innovating!

Competition: HACKRIETJ

Organization: Rajasthan Institute of Engineering and Technology, Jaipur.
'''

msg.attach(MIMEText(body, 'plain'))

# filename = 'Hackhathon 2021 template.pptx'
# attachment = open(filename, "rb")

# p = MIMEBase('application', 'octet-stream')
# p.set_payload((attachment).read())
# encoders.encode_base64(p)
# p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
# msg.attach(p)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(fromaddr, "heyvix999@")

text = msg.as_string()
s.sendmail(fromaddr, toaddr, text)
s.quit()

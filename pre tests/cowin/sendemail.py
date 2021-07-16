# Turn ON this...
# https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4Nr-cE8QbO3xnA0PuHG2regofVD-TQMQzdCLV-4vlaJkS64k33ZgTWGY7dIhRxBJggs_iNb4gBjz7J9LU9evV4rEuQbDA

# Python code to illustrate Sending mail from
# your Gmail account

def send(sub = 'COVID19 Slot Notification',
         data = '...DATA...',
         mailto = 'hellovickykumar123@gmail.com'):

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    import smtplib

    msg = MIMEMultipart()
    msg['From'] = 'imvickykumar999@gmail.com'
    msg['To'] = mailto
    msg['Subject'] = sub

    body = f"Sent using python code by vicks, Slots is {data}"
    msg.attach(MIMEText(body,'plain'))

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('imvickykumar999@gmail.com','Hellovix999@')
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

# send()

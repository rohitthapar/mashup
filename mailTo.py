from email import message
import os 
from email.message import EmailMessage
from re import sub
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.audio import MIMEAudio
from pathlib import Path

email_sender = 'rohit206thapar@gmail.com'
password = 'viohznyupsttwxen'
email_receiver = 'thaprt206@gmail.com'

subject = "Mashup"
body = """ 
    Please find the below attachment 
"""

message = MIMEMultipart()
message['from'] = email_sender
message['to'] = email_receiver
message['subject'] = "test"
message.attach(MIMEText("Body"))
message.attach(MIMEAudio(Path("new.mp3").read_bytes(), 'rb'))

with smtplib.SMTP(host="smtp.gmail.com", port = 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email_sender, password)
    smtp.send_message(message)
    print("Sent....")
# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_receiver
# em['Subject'] = subject
# em.set_content(body)
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context  = context) as smtp:
#     smtp.login(email_sender, password)
#     smtp.sendmail(email_sender , email_receiver, em.as_string())

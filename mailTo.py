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
from pathlib import Path
from zipfile import ZipFile

with ZipFile('nzip.zip', 'w') as zip_file:
    zip_file.write('new1.mp3')

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


with open('nzip.zip', 'rb') as f:
    part = MIMEBase('application', "octet-stream")
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='nzip.zip')
    message.attach(part)

with smtplib.SMTP(host="smtp.gmail.com", port = 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email_sender, password)
    smtp.sendmail(email_sender, email_receiver, message.as_string())
    print("Sent....")

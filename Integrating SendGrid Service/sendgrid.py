


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

message = Mail( from_email='19cs@psgitech.ac.in', 
                to_emails='19cs@psgitech.ac.in',
                subject='Sending a sample email to myself lol',
                plain_text_content='BMR is sending an email via sendgrid with python.',
                html_content='<strong> BMR has received an email.</strong>' )
try:
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)
    print(response.status_code)      
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)   

#!/usr/bin/env python3

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import random

from apiclient import errors
import base64
from email.mime.text import MIMEText
import mimetypes
import os
import random

from twilio.rest import Client

def otp_sms():
    # Your Account SID from twilio.com/console
    account_sid = "AC667937816c391f48f14ffa8e5fcf6f7c"
    # Your Auth Token from twilio.com/console
    auth_token  = "a50915b42ffe3eacd88affdcba243cf5"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+917014195821",
        from_="+19794645484",
        body="OTP AB-456789!")
    print(message.status)

SCOPES = 'https://www.googleapis.com/auth/gmail.send'

def gencode():
    alp = chr(random.randint(65,91))
    alp += chr(random.randint(65,91))
    alp += '-'
    alp += str(random.randint(1, 9999999))
    return alp

def create_message(sender, to, subject, alp):
    s = '''
        Your verification code is %s for activating FabCabHyd account.
        Please do not disclose your verification code to anyone.
    '''
    message = MIMEText(s % alp)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    smsg =  message.as_string()
    smsg = base64.b64encode(smsg.encode())
    smsg = smsg.decode()
    return {'raw': smsg}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def otp_send(destEmail=None):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    c = gencode()

    m = create_message('fabcab@gmail.com', destEmail, 'FabCabHyd Email Verification Code', c)
    print(type(m))
    send_message(service, 'fabcabhyd@gmail.com', m)
    return c
    
if __name__ == '__main__':
    otp_send('vishal.chugh@students.iiit.ac.in')

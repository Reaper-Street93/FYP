import os
import sys
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print("Error: 'credentials.json' file not found. Please download it from your Google Cloud Console and place it in this directory.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text):
   
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
   
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent successfully! Message Id: {sent_message['id']}")
        return sent_message
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def send_email(sender, recipient, subject, message_text):
   
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    message = create_message(sender, recipient, subject, message_text)
    send_message(service, "me", message)

def main():
    sender = "sebastianbarclay0@gmail.com"
    recipient = "sebastianbarclay0@gmail.com"       
    subject = "Dormancy Notice for Your Caxton Account"
    message_text = """Dear John,

We’ve noticed that you haven’t used your Caxton account for the past 9 months. Since your account holds a balance, we want to make you aware of our policy regarding dormant accounts.If your account remains inactive for 12 consecutive months, a dormancy fee of £2 per month will be charged starting from the 12th month of inactivity.To avoid these fees, simply complete any one of the following actions before 28/06/2025:

Load your account – add funds to your Caxton account.

Switch your balance – transfer your balance to another currency.

Use your card for a payment – 
make a purchase using your Caxton card.

These small actions will ensure your account stays active and prevent dormancy fees from being applied.If you need any help or have questions, please don’t hesitate to contact us.

Caxton
"""
    
    send_email(sender, recipient, subject, message_text)

if __name__ == "__main__":
    main()

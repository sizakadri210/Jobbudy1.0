import os.path
import base64
import re
from email import message_from_bytes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid token, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_job_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', q="subject:application OR subject:applied", maxResults=50).execute()
    messages = results.get('messages', [])

    job_data = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_detail['payload']
        headers = payload.get("headers", [])

        subject = sender = date = None
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            elif d['name'] == 'From':
                sender = d['value']
            elif d['name'] == 'Date':
                date = d['value']

        job_data.append({
            'Subject': subject,
            'From': sender,
            'Date': date
        })
    return job_data

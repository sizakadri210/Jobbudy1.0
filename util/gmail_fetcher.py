import streamlit as st
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = Credentials(
        token=None,
        refresh_token=st.secrets["gmail"]["refresh_token"],
        client_id=st.secrets["gmail"]["client_id"],
        client_secret=st.secrets["gmail"]["client_secret"],
        token_uri='https://oauth2.googleapis.com/token',
        scopes=SCOPES
    )
    creds.refresh(Request())
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_job_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=50).execute()
    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Date', 'Subject', 'From']).execute()
        headers = msg_data.get('payload', {}).get('headers', [])
        email_info = {'Date': None, 'Subject': None, 'From': None}

        for header in headers:
            name = header.get('name', '').lower()
            if name == 'date':
                email_info['Date'] = header.get('value')
            elif name == 'subject':
                email_info['Subject'] = header.get('value')
            elif name == 'from':
                email_info['From'] = header.get('value')

        emails.append(email_info)

    return emails

def fetch_job_emails():
    service = get_gmail_service()
    # ✅ Filter only application-related emails
    results = service.users().messages().list(
        userId='me',
        q="subject:job application OR subject:job applied",
        maxResults=50
    ).execute()
    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['Date', 'Subject', 'From']
        ).execute()
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


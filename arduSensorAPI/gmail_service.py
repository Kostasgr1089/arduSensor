import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(BASE_DIR, 'credentials', 'token.json')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials', 'credentials.json')  # optional for re-auth

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SENDER_EMAIL = 'sv1sjh@gmail.com'  # Replace with your Gmail address


def send_email_oauth2(subject, body, to_email):
    # Load credentials from token.json
    if not os.path.exists(TOKEN_PATH):
        raise Exception(f"Token file not found at {TOKEN_PATH}. Please run authorize_gmail.py.")

    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # Refresh the token if expired
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed credentials
            with open(TOKEN_PATH, 'w') as token_file:
                token_file.write(creds.to_json())
        except RefreshError as e:
            raise Exception("OAuth2 token has expired or been revoked. Please reauthorize.") from e

    # Build Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Create and encode the email
    message = MIMEText(body)
    message['to'] = to_email
    message['from'] = SENDER_EMAIL
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    send_message = {'raw': raw}

    # Send the message
    try:
        sent = service.users().messages().send(userId="me", body=send_message).execute()
        print(f"✅ Email sent to {to_email}. Message ID: {sent['id']}")
        return sent
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")

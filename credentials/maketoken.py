from google_auth_oauthlib.flow import InstalledAppFlow
import os, json

BASE_DIR = os.path.dirname(__file__)
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

flow = InstalledAppFlow.from_client_secrets_file(
    CREDENTIALS_PATH,
    scopes=SCOPES
)


creds = flow.run_local_server(
    port=8000,
    access_type='offline',
    prompt='consent'
)



with open(TOKEN_PATH, 'w') as token_file:
    token_file.write(creds.to_json())

print("✅ Token saved.")

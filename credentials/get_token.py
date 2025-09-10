import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')

# Define the required Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Check if credentials.json exists
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"Missing credentials.json at: {CREDENTIALS_PATH}")

# Optionally remove old token.json to force fresh grant
if os.path.exists(TOKEN_PATH):
    print("⚠️  Warning: Old token.json will be deleted to force re-authorization.")
    os.remove(TOKEN_PATH)

# Run the OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    CREDENTIALS_PATH,
    scopes=SCOPES
)

creds = flow.run_local_server(
    port=8000,
    access_type='offline',       # <-- critical to get refresh token
    prompt='consent',            # <-- critical to force refresh token every time
)

# Save the token to a local file
with open(TOKEN_PATH, 'w') as token_file:
    token_file.write(creds.to_json())

print("✅ New token saved successfully to token.json.")

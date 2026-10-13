import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open(r'C:\Users\crypt\.gdrive-mcp\credentials.json') as f:
    token_data = json.load(f)
with open(r'C:\Users\crypt\.gdrive-mcp\gcp-oauth.keys.json') as f:
    client_data = json.load(f)['web']

creds = Credentials(
    token=token_data.get('access_token'),
    refresh_token=token_data.get('refresh_token'),
    token_uri=client_data.get('token_uri'),
    client_id=client_data.get('client_id'),
    client_secret=client_data.get('client_secret'),
    scopes=token_data.get('scope').split()
)

sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

spreadsheet = {
    'properties': {
        'title': 'Traceflow_15_Qualified_SME_Prospects'
    }
}
ss = sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId,spreadsheetUrl').execute()
sheet_id = ss.get('spreadsheetId')
sheet_url = ss.get('spreadsheetUrl')
print(f"Created Sheet: {sheet_id}")
print(f"URL: {sheet_url}")

# Set permission to anyone with link view
permission = {
    'type': 'anyone',
    'role': 'reader'
}
drive_service.permissions().create(
    fileId=sheet_id,
    body=permission,
    fields='id'
).execute()
print("Link sharing set to anyone with link can view successfully!")

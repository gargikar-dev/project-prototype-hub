import os
import sys
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CRED_PATH = r"C:\Users\crypt\.gdrive-mcp\credentials.json"
OAUTH_KEYS_PATH = r"C:\Users\crypt\.gdrive-mcp\gcp-oauth.keys.json"

def main():
    print("Starting OAuth flow...")
    flow = InstalledAppFlow.from_client_secrets_file(
        OAUTH_KEYS_PATH,
        scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    
    # Run local server on port 3000
    creds = flow.run_local_server(port=3000, prompt='consent', access_type='offline')
    
    # Save credentials
    token_dict = {
        'access_token': creds.token,
        'refresh_token': creds.refresh_token,
        'scope': ' '.join(creds.scopes),
        'token_type': 'Bearer'
    }
    with open(CRED_PATH, 'w') as f:
        json.dump(token_dict, f, indent=2)
    print("Credentials saved successfully!")
    
    # Create Google Spreadsheet
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
    print(f"SHEET_ID: {sheet_id}")
    print(f"SHEET_URL: {sheet_url}")
    
    # Set permission to anyone with link view
    drive_service.permissions().create(
        fileId=sheet_id,
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()
    
    # Load prospects from CSV
    import csv
    csv_path = r"c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\Traceflow_15_Qualified_SME_Prospects.csv"
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Sheet1!A1",
        valueInputOption="USER_ENTERED",
        body={"values": reader}
    ).execute()
    
    # Formatting: Freeze header row, format headers
    requests = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": 0,
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                },
                "fields": "gridProperties.frozenRowCount"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.06, "green": 0.32, "blue": 0.20},
                        "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 10},
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
            }
        }
    ]
    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": requests}
    ).execute()
    
    print("SUCCESS: Google Sheet fully populated and formatted!")
    with open(r"c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\created_sheet_url.txt", "w") as f:
        f.write(sheet_url)

if __name__ == "__main__":
    main()
